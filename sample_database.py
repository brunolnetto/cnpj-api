import os
from typing import List, Optional, Tuple, Dict

from sqlalchemy import text
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor, as_completed

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

# -------------------------------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------------------------------------------------

def get_columns(session: Session, table_name: str) -> List[str]:
    """
    Return list of column names in `table_name`, in ordinal_position order.
    """
    query = text("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_schema = 'public'
          AND table_name = :tbl
        ORDER BY ordinal_position
    """)
    result = session.execute(query, {"tbl": table_name})
    return [row[0] for row in result.fetchall()]

def get_create_database(db_name: str) -> str:
    """
    Return a CREATE DATABASE statement (no IF NOT EXISTS for simplicity).
    """
    return f"CREATE DATABASE {db_name};\n"

def get_create_table_query(session: Session, table_name: str) -> str:
    """
    Build a `CREATE TABLE IF NOT EXISTS ... (col TEXT, ...)` statement 
    by inspecting column names. All types are TEXT for the dump.
    """
    columns = get_columns(session, table_name)
    if not columns:
        return ""
    col_defs = ", ".join(f"{col} TEXT" for col in columns)
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs});\n"

def get_index_definitions(session: Session, table_name: str) -> List[str]:
    """
    Query pg_indexes to retrieve the index DDL for all indexes on `table_name`.
    Returns a list of strings, each being a `CREATE INDEX ...;` statement.
    """
    idx_query = text("""
        SELECT indexdef
        FROM pg_indexes
        WHERE schemaname = 'public'
          AND tablename = :tbl
    """)
    result = session.execute(idx_query, {"tbl": table_name})
    return [row[0].strip() + ";\n" for row in result.fetchall()]

def fetch_table_data(
    session_maker,
    table_name: str,
    key_list: Optional[List[str]],
) -> Tuple[str, List[str], List[Dict[str, Optional[str]]]]:
    """
    In a new Session, run a SELECT on `table_name` (filtered by key_list if provided),
    and return: (table_name, column_names, list_of_row_dicts).
    Each row_dict maps column_name -> Python value (or None).
    """
    with session_maker() as session:
        # 1. Get column names once
        columns = get_columns(session, table_name)
        if not columns:
            # No columns => empty table? return empty result set
            return table_name, [], []

        cols_joined = ", ".join(columns)
        if key_list is None:
            select_sql = text(f"SELECT {cols_joined} FROM {table_name};")
            params = {}
        else:
            select_sql = text(f"""
                SELECT {cols_joined}
                FROM {table_name}
                WHERE cnpj_basico = ANY(:keys)
            """)
            params = {"keys": key_list}

        result = session.execute(select_sql, params).fetchall()

        # Convert each row (RowMapping) into a simple dict {col: value}
        rows = []
        for row in result:
            row_map = dict(row._mapping)
            rows.append(row_map)

        return table_name, columns, rows

def escape_sql_value(val) -> str:
    """
    Escape a single Python value into a SQL literal.
    - None -> NULL
    - Otherwise, convert to string, escape single quotes by doubling them.
    """
    if val is None:
        return "NULL"
    s = str(val).replace("'", "''")
    return f"'{s}'"

# -------------------------------------------------------------------------------------------------
# MAIN DUMP FUNCTION
# -------------------------------------------------------------------------------------------------

def create_sample_sql_dump(
    session_maker,            # now we pass the factory, not an active session
    sample_db_name: str,
    sample_size: int,
    output_sql_file: str,
    max_workers: int = 4,
    batch_size: int = 500
):
    """
    1. Delete any existing dump file.
    2. Write a CREATE DATABASE statement.
    3. Using a root Session, sample `empresa` once to get N distinct cnpj_basico keys.
    4. Fetch (columns, rows) for each relevant table in parallel threads:
       - "empresa"       (filtered by those keys)
       - "estabelecimento", "socios", "simples" (all filtered by the same keys)
       - "cnae", "natju", "moti", "munic", "pais", "quals" (no filter: full table)
    5. Once all data is in memory, write out:
       a) CREATE TABLE IF NOT EXISTS ...
       b) CREATE INDEX ... for that table
       c) Bulk multi‐row INSERT statements in batches.
    6. Print progress feedback at each major step.
    """

    # 0. Remove old file if it exists
    if os.path.exists(output_sql_file):
        os.remove(output_sql_file)

    # 1. Write CREATE DATABASE
    with open(output_sql_file, "a") as f:
        f.write(get_create_database(sample_db_name))
    print(f"[1/5] Wrote CREATE DATABASE to '{output_sql_file}'")

    # 2. Sample `empresa` using a short-lived Session
    with session_maker() as root_session:
        print(f"[2/5] Sampling {sample_size} keys from 'empresa'…")
        root_session.execute(text("SELECT setseed(0.123456);"))
        empresa_sample_q = text("""
            SELECT cnpj_basico
            FROM empresa
            ORDER BY RANDOM()
            LIMIT :limit_count
        """)
        empresa_keys = [
            row[0]
            for row in root_session.execute(empresa_sample_q, {"limit_count": sample_size})
        ]
        print(f"      → Retrieved {len(empresa_keys)} keys from 'empresa'")

    # 3. Prepare the list of tables and their key filters
    filtered_tables = ["empresa", "estabelecimento", "socios", "simples"]
    lookup_tables   = ["cnae", "natju", "moti", "munic", "pais", "quals"]

    # Build a map: table_name -> (key_list or None)
    table_filters: Dict[str, Optional[List[str]]] = {
        tbl: list(empresa_keys) for tbl in filtered_tables
    }
    for tbl in lookup_tables:
        table_filters[tbl] = None

    # 4. Fetch all tables’ data concurrently with ThreadPoolExecutor
    print(f"[3/5] Fetching data for {len(table_filters)} tables in parallel…")
    fetched_data: Dict[str, Tuple[List[str], List[Dict[str, Optional[str]]]]] = {}
    futures = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for tbl, keys in table_filters.items():
            fut = executor.submit(fetch_table_data, session_maker, tbl, keys)
            futures.append(fut)

        for fut in as_completed(futures):
            tbl_name, columns, rows = fut.result()
            fetched_data[tbl_name] = (columns, rows)
            print(f"      → Fetched {len(rows)} rows from '{tbl_name}' (cols: {len(columns)})")

    # 5. Write DDL + indexes + bulk INSERTs in a deterministic order
    print(f"[4/5] Writing DDL, indexes, and bulk INSERTs to '{output_sql_file}'…")

    def write_table_to_file(
        tbl: str,
        columns: List[str],
        rows: List[Dict[str, Optional[str]]],
        file_path: str,
    ):
        """
        Append to file:
        a) CREATE TABLE IF NOT EXISTS ...
        b) CREATE INDEX ... ; (one per index)
        c) Bulk multi‐row INSERT in batches of `batch_size`
        """
        with open(file_path, "a") as f:
            # a) CREATE TABLE
            create_sql = get_create_table_query(root_session, tbl)
            f.write(create_sql)

            # b) CREATE INDEX statements
            idx_ddls = get_index_definitions(root_session, tbl)
            for ddl in idx_ddls:
                f.write(ddl)

            # c) Bulk INSERT rows
            if not columns or not rows:
                return

            col_list = ", ".join(columns)
            total = len(rows)
            for start in range(0, total, batch_size):
                chunk = rows[start : start + batch_size]
                values_list = []
                for row_map in chunk:
                    escaped = [escape_sql_value(row_map[c]) for c in columns]
                    values_list.append("(" + ", ".join(escaped) + ")")
                joined_values = ",\n  ".join(values_list)
                insert_stmt = (
                    f"INSERT INTO {tbl} ({col_list})\n"
                    f"VALUES\n  {joined_values};\n"
                )
                f.write(insert_stmt)

    # Ensure the same order: filtered_tables first, then lookup_tables
    write_order = filtered_tables + lookup_tables
    total_tables = len(write_order)
    for idx, tbl in enumerate(write_order, start=1):
        cols, rows = fetched_data[tbl]
        print(f"      [4/{total_tables}] Writing '{tbl}' → {len(rows)} rows…")
        write_table_to_file(tbl, cols, rows, output_sql_file)

    print(f"[5/5] Dump complete. '{output_sql_file}' is ready to be loaded.")

# -------------------------------------------------------------------------------------------------
# USAGE EXAMPLE (if run as a script)
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    from_database = multi_database.databases[settings.POSTGRES_DBNAME_RFB]
    session_maker = from_database.session_maker  # the factory for creating new Session

    sample_db_name = "dadosrfb_sample"
    output_file   = "sample_data.sql"
    sample_size   = 100

    create_sample_sql_dump(
        session_maker=session_maker,
        sample_db_name=sample_db_name,
        sample_size=sample_size,
        output_sql_file=output_file,
        max_workers=4,    # Number of parallel threads to fetch table data
        batch_size=100    # Rows per bulk-insert statement
    )
