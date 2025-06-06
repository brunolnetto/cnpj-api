import os
import gzip
import time
import logging
import uuid
import decimal
import datetime
from typing import List, Optional, Tuple, Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session
from sqlalchemy.engine import Result
from sqlalchemy.exc import OperationalError
from rich.logging import RichHandler
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn

from backend.app.database.base import multi_database
from backend.app.setup.config import settings

# Setup rich logging with optional verbosity from environment
verbose = os.getenv("DUMP_VERBOSE", "0") == "1"
logging.basicConfig(
    level=logging.DEBUG if verbose else logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger("sql_dump")

# -------------------------------------------------------------------------------------------------
# UTILITY FUNCTIONS
# -------------------------------------------------------------------------------------------------

def retry(exceptions, tries=3, delay=1, backoff=2):
    """Retry decorator with exponential backoff."""
    def decorator_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f"[yellow]Retry {func.__name__} due to {e}, attempts left: {mtries-1}[/yellow]")
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator_retry

def quote_identifier(session: Session, identifier: str) -> str:
    # Use SQLAlchemy's quoting to avoid SQL injection and quoting issues
    return session.bind.dialect.identifier_preparer.quote(identifier)

def get_columns(session: Session, table_name: str, schema: str = "public") -> List[str]:
    insp = inspect(session.bind)
    try:
        cols = insp.get_columns(table_name, schema)
        return [col["name"] for col in cols]
    except Exception as e:
        logger.error(f"Failed to get columns for {schema}.{table_name}: {e}")
        return []

def get_index_definitions(session: Session, table_name: str, schema: str = "public") -> List[str]:
    query = text("""
        SELECT indexdef
        FROM pg_indexes
        WHERE schemaname = :schema AND tablename = :tbl
    """)
    result: Result = session.execute(query, {"schema": schema, "tbl": table_name})
    return [row[0].strip() + ";\n" for row in result.fetchall()]

def get_create_database(db_name: str) -> str:
    if not db_name.isidentifier():
        raise ValueError(f"Invalid database name: {db_name}")
    return f"CREATE DATABASE {db_name};\n\n"

def get_create_table_query(session: Session, table_name: str, schema: str = "public") -> str:
    columns = get_columns(session, table_name, schema)
    if not columns:
        return ""
    # WARNING: This is a simplification! You should extract actual column types from DB if you want real dumps
    quoted_cols = ", ".join(f"{quote_identifier(session, col)} TEXT" for col in columns)
    quoted_tbl = f"{quote_identifier(session, schema)}.{quote_identifier(session, table_name)}"
    return f"CREATE TABLE IF NOT EXISTS {quoted_tbl} ({quoted_cols});\n\n"

def escape_sql_value(val: Any) -> str:
    if val is None:
        return "NULL"
    if isinstance(val, bool):
        return "TRUE" if val else "FALSE"
    if isinstance(val, (int, float)):
        return str(val)
    if isinstance(val, datetime.datetime):
        return f"'{val.isoformat(sep=' ', timespec='seconds')}'"
    if isinstance(val, datetime.date):
        return f"'{val.isoformat()}'"
    if isinstance(val, uuid.UUID):
        return f"'{str(val)}'"
    if isinstance(val, decimal.Decimal):
        return str(val)
    if isinstance(val, str):
        # Escape single quotes for SQL strings
        return f"'{val.replace('\'', '\'\'')}'"
    return f"'{str(val).replace('\'', '\'\'')}'"

@retry((OperationalError,), tries=3, delay=1)
def fetch_table_data(
    session_maker: Callable[[], Session],
    table_name: str,
    key_list: Optional[List[Any]] = None,
    key_column: str = "cnpj_basico",
    chunk_size: int = 5000,
    schema: str = "public",
) -> Tuple[str, List[str], List[Dict[str, Any]]]:
    rows: List[Dict[str, Any]] = []

    with session_maker() as session:
        columns = get_columns(session, table_name, schema)
        if not columns:
            return table_name, [], []

        quoted_cols = ", ".join(quote_identifier(session, col) for col in columns)
        quoted_tbl = f"{quote_identifier(session, schema)}.{quote_identifier(session, table_name)}"

        if key_list:
            query = text(f"""
                SELECT {quoted_cols}
                FROM {quoted_tbl}
                WHERE {quote_identifier(session, key_column)} = ANY(:keys)
            """)
            params = {"keys": key_list}
        else:
            query = text(f"SELECT {quoted_cols} FROM {quoted_tbl};")
            params = {}

        result = session.execute(query, params)
        # Use fetchmany to limit memory footprint, yield rows incrementally
        while True:
            chunk = result.fetchmany(chunk_size)
            if not chunk:
                break
            rows.extend(dict(row._mapping) for row in chunk)

    return table_name, columns, rows

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
    schema: str = "public",
    compress_output: bool = False,
):
    if os.path.exists(output_sql_file):
        os.remove(output_sql_file)

    open_func = gzip.open if compress_output else open
    mode = "wt"

    with session_maker() as root_session:
        logger.info(f"[bold cyan]Starting dump of database: {sample_db_name}[/bold cyan]")

        with open_func(output_sql_file, mode, encoding="utf-8") as f:
            f.write(get_create_database(sample_db_name))
        logger.info(f"Wrote CREATE DATABASE statement to '{output_sql_file}'")

        logger.info(f"Sampling {sample_size} keys from 'empresa'...")
        start_sample = time.perf_counter()
        root_session.execute(text("SELECT setseed(0.123456);"))
        sample_keys_q = text(f"""
            SELECT cnpj_basico
            FROM {quote_identifier(root_session, schema)}.empresa
            TABLESAMPLE SYSTEM (0.1)
            LIMIT :limit_count
        """)
        empresa_keys = [row[0] for row in root_session.execute(sample_keys_q, {"limit_count": sample_size})]
        duration_sample = time.perf_counter() - start_sample
        logger.info(f"Retrieved {len(empresa_keys)} keys from 'empresa' in {duration_sample:.2f}s")

    filtered_tables = ["empresa", "estabelecimento", "socios", "simples"]
    lookup_tables = ["cnae", "natju", "moti", "munic", "pais", "quals"]

    table_filters: Dict[str, Optional[List[Any]]] = {tbl: empresa_keys.copy() for tbl in filtered_tables}
    table_filters.update({tbl: None for tbl in lookup_tables})

    fetched_data: Dict[str, Tuple[List[str], List[Dict[str, Any]]]] = {}

    logger.info(f"Fetching data concurrently for {len(table_filters)} tables with {max_workers} workers...")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
    ) as progress:
        task_fetch = progress.add_task("Fetching tables...", total=len(table_filters))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(fetch_table_data, session_maker, tbl, keys, schema=schema): tbl
                for tbl, keys in table_filters.items()
            }
            for future in as_completed(futures):
                tbl_name = futures[future]
                try:
                    tbl, cols, rows = future.result()
                    fetched_data[tbl] = (cols, rows)
                    logger.info(f"Fetched {len(rows)} rows from '{tbl_name}' (columns: {len(cols)})")
                except Exception as e:
                    logger.exception(f"Failed to fetch data for table '{tbl_name}': {e}")
                    fetched_data[tbl_name] = ([], [])
                progress.update(task_fetch, advance=1)

    # Write output in append mode, streaming batches to minimize memory usage
    with session_maker() as session, open_func(output_sql_file, "at", encoding="utf-8") as f:
        logger.info("[bold cyan]Writing tables and data to output file...[/bold cyan]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            transient=True,
        ) as task_write:
            task = task_write.add_task("Writing tables...", total=len(fetched_data))
            for table, (columns, rows) in fetched_data.items():
                if not columns:
                    logger.warning(f"No columns found for table {table}, skipping.")
                    task_write.advance(task)
                    continue

                # Write CREATE TABLE statement
                f.write(get_create_table_query(session, table, schema))
                if rows:
                    tbl_qualified = f"{quote_identifier(session, schema)}.{quote_identifier(session, table)}"
                    quoted_cols = ", ".join(quote_identifier(session, col) for col in columns)

                    # Write INSERT statements in batches
                    for i in range(0, len(rows), batch_size):
                        batch_rows = rows[i : i + batch_size]
                        # Build values string incrementally, streaming to file (avoid large concatenation)
                        f.write(f"INSERT INTO {tbl_qualified} ({quoted_cols}) VALUES\n")
                        for idx, row in enumerate(batch_rows):
                            escaped_values = [escape_sql_value(row.get(col)) for col in columns]
                            values_str = f"({', '.join(escaped_values)})"
                            if idx < len(batch_rows) - 1:
                                values_str += ",\n"
                            else:
                                values_str += ";\n"
                            f.write(values_str)

                task_write.advance(task)

            # Write indexes after all inserts
            logger.info("Writing indexes...")
            for table in fetched_data.keys():
                idx_defs = get_index_definitions(session, table, schema)
                for idx_stmt in idx_defs:
                    f.write(idx_stmt)

    logger.info(f"[bold green]SQL dump creation finished: {output_sql_file}[/bold green]")


# -------------------------------------------------------------------------------------------------
# USAGE EXAMPLE (if run as a script)
# -------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    from_database = multi_database.databases[settings.POSTGRES_DBNAME_RFB]
    print(f"Using database: {settings.POSTGRES_DBNAME_RFB}")
    session_maker = from_database.session_maker  # factory for creating new Session

    from dotenv import load_dotenv
    from os import environ
    load_dotenv('.env.dev')

    sample_db_name = environ.get("POSTGRES_DBNAME_RFB")
    print(f"Sample database name: {sample_db_name}")
    output_file = "data/sample_data.sql"
    sample_size = 100

    create_sample_sql_dump(
        session_maker=session_maker,
        sample_db_name=sample_db_name,
        sample_size=sample_size,
        output_sql_file=output_file,
        max_workers=8,    # Number of parallel threads to fetch table data
        batch_size=100    # Rows per bulk-insert statement
    )
