from typing import Dict, Optional, ContextManager, Any
from contextlib import contextmanager
from sqlalchemy.orm import Session

from psycopg2 import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, inspect, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.engine.url import make_url

from backend.app.setup.config import settings


class BaseDatabase:
    def get_session(self) -> ContextManager:
        raise NotImplementedError()

    def create_database(self):
        raise NotImplementedError()

    def test_connection(self):
        raise NotImplementedError()

    def create_tables(self):
        raise NotImplementedError()

    def print_tables(self):
        raise NotImplementedError()


class Database(BaseDatabase):
    """
    Database class for managing PostgreSQL database connections and operations.
    """

    def __init__(self, uri: str):
        if not uri:
            raise ValueError("Database URI must be provided.")

        self.url = make_url(uri)
        self.base = declarative_base()
        self.engine = create_engine(
            uri,
            pool_size=30,
            max_overflow=20,
            pool_timeout=60,
            pool_recycle=1800,
            pool_pre_ping=True,
            isolation_level="AUTOCOMMIT",
        )
        self.session_maker = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self) -> ContextManager[Session]:
        """Context manager to get a database session."""
        session = self.session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def mask_sensitive_data(self) -> str:
        """Masks sensitive data in the database URI."""
        masked_uri = self.url.set(password="******") if self.url.password else self.url
        return str(masked_uri)

    def create_database(self):
        masked_uri = self.mask_sensitive_data()
        try:
            with self.engine.begin() as conn:
                query = text("SELECT 1 FROM pg_database WHERE datname = :dbname")
                db_data = {"dbname": self.url.database}
                result = conn.execute(query, db_data)

                if not result.scalar():
                    conn.execute(text(f"CREATE DATABASE {self.url.database}"))
                    print(f"Database {masked_uri} created!")
                else:
                    print(f"Database {masked_uri} already exists!")
        except OperationalError as e:
            print(f"Error creating database {masked_uri}: {e}")

    def test_connection(self):
        masked_uri = self.mask_sensitive_data()
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print(f"Connection to the database {masked_uri} established!")
        except OperationalError as e:
            print(f"Error connecting to the database {masked_uri}: {e}")

    def create_tables(self):
        """Creates tables in the database based on the defined models."""
        masked_uri = self.mask_sensitive_data()
        try:
            with self.engine.begin() as conn:
                self.base.metadata.create_all(conn)
            print(f"Tables for database {masked_uri} created!")
        except SQLAlchemyError as e:
            print(f"Error creating tables in the database {masked_uri}: {e}")

    def print_tables(self):
        """Print the available tables in the database."""
        masked_uri = self.mask_sensitive_data()
        try:
            with self.engine.connect() as conn:
                inspector = inspect(conn)
                tables = inspector.get_table_names()
                print(f"Available tables in {masked_uri}: {tables}")
        except Exception as e:
            print(f"Error fetching table names from {masked_uri}: {e}")

    def init(self):
        """Initializes the database connection and creates the tables."""
        self.create_database()
        self.test_connection()
        self.create_tables()
        self.print_tables()

    def disconnect(self):
        """Clean up and close the database connection and session maker."""
        masked_uri = self.mask_sensitive_data()
        try:
            self.session_maker.close_all()
            self.engine.dispose()
            print(f"Database {masked_uri} connections closed.")
        except Exception as e:
            print(f"Error closing database connections: {e}")

    def __str__(self) -> str:
        return f"Database(uri={self.mask_sensitive_data()}, engine={self.engine})"

    def __repr__(self) -> str:
        masked_uri = self.mask_sensitive_data()
        return f"<Database(uri={masked_uri})>"


class MultiDatabase(BaseDatabase):
    """
    This class represents a multi-database connection and session management object.
    """

    def __init__(self, database_uris: Dict[str, str]):
        if not database_uris:
            raise ValueError("Database URIs must be provided.")

        self.databases = {
            db_name: Database(uri) for db_name, uri in database_uris.items()
        }

    @contextmanager
    def get_session(self, db_name: str) -> ContextManager:
        """Get a session for a specific database."""
        if db_name not in self.databases:
            raise ValueError(f"No such database: {db_name}")

        with self.databases[db_name].get_session() as session:
            yield session

    def create_database(self):
        """Create databases for all configured databases."""
        for database in self.databases.values():
            database.create_database()

    def test_connection(self):
        """Test connection for all configured databases."""
        for database in self.databases.values():
            database.test_connection()

    def create_tables(self):
        """Create tables for all configured databases."""
        for database in self.databases.values():
            database.create_tables()

    def print_tables(self):
        """Print the available tables in all databases."""
        for database in self.databases.values():
            database.print_tables()

    def init(self):
        """Initialize all databases concurrently."""
        for database in self.databases.values():
            try:
                database.init()
            except Exception as e:
                print(f"Error during initialization of {database}: {e}")

    def disconnect(self):
        """Disconnect all databases concurrently."""
        for database in self.databases.values():
            database.disconnect()


# Load environment variables from the .env file
multi_database: Optional[MultiDatabase] = MultiDatabase(settings.postgres_uris_dict)


def init_database():
    """Initialize the multi-database setup."""
    multi_database.init()


@contextmanager
def get_session(db_name: str) -> ContextManager:
    """Define a dependency to create a database session."""
    if multi_database is None:
        init_database()

    try:
        with multi_database.get_session(db_name) as session:
            yield session
    except SQLAlchemyError as e:
        print(f"Failed to get session for {db_name}: {e}")
        raise
