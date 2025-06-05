import os
import logging
from typing import List, Optional, Tuple, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

# Configure logging instead of print
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------------------------------------------------

def quote_identifier(identifier: str) -> str:
    """
    Safely quote SQL identifiers (table names, column names) using double quotes.
    Assumes standard SQL identifiers without double quotes inside.
    """
    if not identifier.isidentifier():
        raise ValueError(f"Unsafe SQL identifier: {identifier}")
    return f'"{identifier}"'

def get_columns(session: Session, table_name: str) -> List[str]:
    """
    Return list of column names in `table_name` in ordinal_position order.
    """
    query = text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public' AND table_name = :tbl
        ORDER BY ordinal_position
    """)
    result: Result = session.execute(query, {"tbl": table_name})
    columns = [row[0] for row in result.fetchall()]
    return columns

def get_create_database(db_name: str) -> str:
    """
    Return a CREATE DATABASE statement.
    """
    # No quoting to keep simple, but consider validating db_name before
    if not db_name.isidentifier():
        raise ValueError(f"Invalid database name: {db_name}")
    return f"CREATE DATABASE {db_name};\n"

def get_create_table_query(session: Session, table_name: str) -> str:
    """
    Build CREATE TABLE IF NOT EXISTS ... (col TEXT, ...) statement by inspecting column names.
    All types are TEXT for the dump.
    """
    columns = get_columns(session, table_name)
    if not columns:
        return ""
    quoted_cols = ", ".join(f"{quote_identifier(col)} TEXT" for col in columns)
    quoted_tbl = quote_identifier(table_name)
    return f"CREATE TABLE IF NOT EXISTS {quoted_tbl} ({quoted_cols});\n"

def get_index_definitions(session: Session, table_name: str) -> List[str]:
    """
    Query pg_indexes to retrieve index DDL for all indexes on `table_name`.
    Returns a list of CREATE INDEX statements.
    """
    query = text("""
        SELECT indexdef
        FROM pg_indexes
        WHERE schemaname = 'public' AND tablename = :tbl
    """)
    result: Result = session.execute(query, {"tbl": table_name})
    return [row[0].strip() + ";\n" for row in result.fetchall()]

def fetch_table_data(
    session_maker: Callable[[], Session],
    table_name: str,
    key_list: Optional[List[Any]] = None,
    key_column: str = "cnpj_basico",
    chunk_size: int = 5000,
) -> Tuple[str, List[str], List[Dict[str, Any]]]:
    """
    Run SELECT on `table_name` (filtered by key_list if provided),
    return: (table_name, column_names, list_of_row_dicts).

    Fetches data in chunks to avoid memory spikes.
    """
    columns: List[str]
    rows: List[Dict[str, Any]] = []

    with session_maker() as session:
        columns = get_columns(session, table_name)
        if not columns:
            return table_name, [], []

        quoted_cols = ", ".join(quote_identifier(col) for col in columns)
        quoted_tbl = quote_identifier(table_name)

        if key_list:
            # Parameterize keys for safer queries (Postgres ANY() works with lists)
            query = text(f"""
                SELECT {quoted_cols}
                FROM {quoted_tbl}
                WHERE {quote_identifier(key_column)} = ANY(:keys)
            """)
            params = {"keys": key_list}
        else:
            query = text(f"SELECT {quoted_cols} FROM {quoted_tbl};")
            params = {}

        # Fetch in chunks to avoid big memory usage
        result = session.execute(query, params)
        for chunk in iter(lambda: result.fetchmany(chunk_size), []):
            for row in chunk:
                rows.append(dict(row._mapping))

    return table_name, columns, rows

def escape_sql_value(val: Any) -> str:
    """
    Escape Python value to SQL literal:
    - None -> NULL
    - str -> quoted with doubled single quotes
    - int/float -> as is
    - bool -> TRUE/FALSE
    - other -> str coerced and quoted
    """
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, str):
        escaped = val.replace("'", "''")
        return f"'{escaped}'"
    # fallback: convert to string and quote
    escaped = str(val).replace("'", "''")
    return f"'{escaped}'"

# -------------------------------------------------------------------------------------------------
# MAIN DUMP FUNCTION
# -------------------------------------------------------------------------------------------------

def create_sample_sql_dump(
    session_maker: Callable[[], Session],
    sample_db_name: str,
    sample_size: int,
    output_sql_file: str,
    max_workers: int = 4,
    batch_size: int = 500,
):
    """
    Create a SQL dump sampling data from specific tables.
    """

    # Remove old file safely
    if os.path.exists(output_sql_file):
        os.remove(output_sql_file)

    with session_maker() as root_session:
        # Write CREATE DATABASE at start (using root_session to be consistent)
        with open(output_sql_file, "w") as f:
            f.write(get_create_database(sample_db_name))
        logger.info(f"Wrote CREATE DATABASE statement to '{output_sql_file}'")

        # Sample keys from empresa table with fixed seed for reproducibility
        logger.info(f"Sampling {sample_size} keys from 'empresa'...")
        root_session.execute(text("SELECT setseed(0.123456);"))
        sample_keys_q = text("""
            SELECT cnpj_basico
            FROM empresa
            ORDER BY RANDOM()
            LIMIT :limit_count
        """)
        empresa_keys = [row[0] for row in root_session.execute(sample_keys_q, {"limit_count": sample_size})]
        logger.info(f"Retrieved {len(empresa_keys)} keys from 'empresa'")

    # Define tables and filters
    filtered_tables = ["empresa", "estabelecimento", "socios", "simples"]
    lookup_tables = ["cnae", "natju", "moti", "munic", "pais", "quals"]

    table_filters: Dict[str, Optional[List[Any]]] = {tbl: empresa_keys.copy() for tbl in filtered_tables}
    for tbl in lookup_tables:
        table_filters[tbl] = None

    # Fetch data concurrently
    logger.info(f"Fetching data concurrently for {len(table_filters)} tables...")
    fetched_data: Dict[str, Tuple[List[str], List[Dict[str, Any]]]] = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_table_data, session_maker, tbl, keys): tbl
            for tbl, keys in table_filters.items()
        }

        for future in as_completed(futures):
            tbl_name = futures[future]
            try:
                tbl, cols, rows = future.result()
                fetched_data[tbl] = (cols, rows)
                logger.info(f"Fetched {len(rows)} rows from '{tbl}' (columns: {len(cols)})")
            except Exception as e:
                logger.error(f"Failed to fetch data for table '{tbl_name}': {e}")
                fetched_data[tbl_name] = ([], [])

    def write_table_to_file(
        table: str,
        columns: List[str],
        rows: List[Dict[str, Any]],
        file_path: str,
        session: Session,
        batch_size: int = 500,
    ):
        """
        Write DDL + indexes + bulk INSERT statements for a single table to file.
        """

        with open(file_path, "a") as f:
            # CREATE TABLE
            create_stmt = get_create_table_query(session, table)
            if create_stmt:
                f.write(create_stmt)
            else:
                logger.warning(f"No columns found for table {table}, skipping DDL and inserts.")
                return

            # Indexes
            indexes = get_index_definitions(session, table)
            for idx_stmt in indexes:
                f.write(idx_stmt)

            # Bulk insert in batches
            if not columns or not rows:
                logger.info(f"No data to insert for table {table}")
                return

            quoted_cols = ", ".join(quote_identifier(c) for c in columns)
            total_rows = len(rows)

            for start in range(0, total_rows, batch_size):
                batch_rows = rows[start : start + batch_size]
                values_sql = ",\n  ".join(
                    "(" + ", ".join(escape_sql_value(row[col]) for col in columns) + ")"
                    for row in batch_rows
                )
                insert_stmt = f"INSERT INTO {quote_identifier(table)} ({quoted_cols})\nVALUES\n  {values_sql};\n"
                f.write(insert_stmt)

    # Write out data in deterministic order
    write_order = filtered_tables + lookup_tables

    logger.info(f"Writing DDL and data for {len(write_order)} tables...")
    with session_maker() as session:
        for idx, tbl in enumerate(write_order, start=1):
            cols, rows = fetched_data.get(tbl, ([], []))
            logger.info(f"[{idx}/{len(write_order)}] Writing table '{tbl}' with {len(rows)} rows...")
            try:
                write_table_to_file(tbl, cols, rows, output_sql_file, session, batch_size=batch_size)
            except Exception as e:
                logger.error(f"Error writing table '{tbl}': {e}")

    logger.info(f"SQL dump creation complete: '{output_sql_file}'")


# -------------------------------------------------------------------------------------------------
# USAGE EXAMPLE (if run as a script)
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    from_database = multi_database.databases[settings.POSTGRES_DBNAME_RFB]
    session_maker = from_database.session_maker  # the factory for creating new Session

    sample_db_name = "dadosrfb_def"
    output_file   = "data/sample_data.sql"
    sample_size   = 100

    create_sample_sql_dump(
        session_maker=session_maker,
        sample_db_name=sample_db_name,
        sample_size=sample_size,
        output_sql_file=output_file,
        max_workers=4,    # Number of parallel threads to fetch table data
        batch_size=100    # Rows per bulk-insert statement
    )
