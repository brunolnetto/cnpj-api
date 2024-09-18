from typing import Dict, Optional, ContextManager
from contextlib import contextmanager
import asyncio

from psycopg2 import OperationalError
from sqlalchemy import text, inspect, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
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


    Attributes:
        url (URL): Parsed database URL.
        base (DeclarativeMeta): SQLAlchemy declarative base.
        engine (Engine): SQLAlchemy engine for database connection.
        session_maker (sessionmaker): SQLAlchemy session maker.

    Methods:
        get_session():
            Context manager to get a database session.
        mask_sensitive_data() -> str:
            Masks sensitive data in the database URI.
        create_database():
            Creates the database if it does not exist.
        test_connection():
            Tests the connection to the database.
        create_tables():
            Creates tables in the database based on the defined models.
        print_tables():
            Prints the available tables in the database.
        init():
        disconnect():
            Cleans up and closes the database connection and session maker.
        __repr__() -> str:
            Returns a string representation of the Database instance with masked URI.
    """    

    def __init__(self, uri):
        self.url = make_url(uri)
        self.base = declarative_base()
        self.engine = create_engine(
            uri,
            poolclass=QueuePool,  # Use connection pooling
            pool_size=20,       # Adjust pool size based on your workload
            max_overflow=10,    # Adjust maximum overflow connections
            pool_recycle=3600,  # Periodically recycle connections (optional)
            isolation_level="AUTOCOMMIT",
        )
        self.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    @contextmanager
    def get_session(self):
        return self.session_maker()

    def mask_sensitive_data(self) -> str:
        # Mask the password if it's present
        if self.url.password:
            parsed_uri = self.url.set(password="******")

            # Return the sanitized URI as a string
            return str(parsed_uri)

        return str(self.url)

    def create_database(self):
        masked_uri = self.mask_sensitive_data()

        try:
            with self.engine.begin() as conn:                
                query = text("SELECT 1 FROM pg_database WHERE datname = :dbname")
                db_data = {"dbname": self.url.database}
                result = conn.execute(query, db_data)
                
                if not result.scalar():
                    query = text(f"CREATE DATABASE {make_url(self.url).database}")
                    conn.execute(query)
                    print(f"Database {masked_uri} created!")
                else:
                    print(f"Database {masked_uri} already exists!")

        except OperationalError as e:
            print(f"Error creating database {masked_uri}: {e}")

    def test_connection(self):
        masked_uri = self.mask_sensitive_data()
        try:
            with self.engine.begin() as conn:
                query = text("SELECT 1")

                # Test the connection
                conn.execute(query)

                print(f"Connection to the database {masked_uri} established!")

        except OperationalError as e:
            print(f"Error connecting to the database {masked_uri}: {e}")

    def create_tables(self):
        """
        Connects to a PostgreSQL database using environment variables for connection details.

        Returns:
            Database: A NamedTuple with engine and conn attributes for the database connection.
            None: If there was an error connecting to the database.

        """
        masked_uri = self.mask_sensitive_data()
        try:
            # Create all tables defined using the Base class (if not already
            # created)
            self.base.metadata.create_all(self.engine)

            print(f"Tables for database {masked_uri} created!")

        except Exception as e:
            print(f"Error creating tables in the database {masked_uri}: {str(e)}")

    def print_tables(self):
        """
        Print the available tables in the database.
        """
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            print(f"Available tables: {tables}")
        except Exception as e:
            print(f"Error fetching table names: {str(e)}")

    async def init(self):
        """
        Initializes the database connection and creates the tables.

        Args:
            uri (str): The database URI.

        Returns:
            Database: A NamedTuple with engine and conn attributes for the database connection.
            None: If there was an error connecting to the database.
        """
        print("#################################################################")
        try:
            self.create_database()
        except Exception as e:
            print(f"Error creating database: {e}")

        try:
            self.test_connection()
        except Exception as e:
            print(f"Error testing connection: {e}")

        try:
            self.create_tables()
        except Exception as e:
            print(f"Error creating tables: {e}")

        try:
            self.print_tables()
        except Exception as e:
            print(f"Error print available tables: {e}")
        print("#################################################################")

    async def disconnect(self):
        """
        Clean up and close the database connection and session maker.
        """
        masked_uri = self.mask_sensitive_data()
        try:
            # Close all connections in the pool
            self.engine.dispose()
            print(f"Database {masked_uri} connections closed.")
        except Exception as e:
            print(f"Error closing database connections: {str(e)}")

    def __repr__(self):
        masked_uri = self.mask_sensitive_data()
        return f"<Database(uri={masked_uri})>"


class MultiDatabase(BaseDatabase):
    """
    This class represents a multi-database connection and session management object.
    It contains methods to handle multiple databases.
    """

    def __init__(self, database_uris: Dict[str, str]):
        """
        Initialize with a dictionary of database URIs.
        """
        self.databases = {
            db_name: Database(uri) for db_name, uri in database_uris.items()
        }

    @contextmanager
    def get_session(self, db_name) -> ContextManager:
        """
        Get a session for a specific database.
        """
        if db_name not in self.databases:
            raise ValueError(f"No such database: {db_name}")

        with self.databases[db_name].session_maker() as session:
            yield session

    def create_database(self):
        for database in self.databases.values():
            database.create_database()

    def test_connection(self):
        for database in self.databases.values():
            database.test_connection()

    def create_tables(self):
        for database in self.databases.values():
            database.create_tables()

    def print_tables(self):
        """
        Print the available tables in a specific database.
        """
        for database in self.databases.values():
            database.print_tables()

    async def init(self):
        """
        Initialize all databases concurrently.
        """
        tasks = [database.init() for database in self.databases.values()]
        await asyncio.gather(*tasks)

    async def disconnect(self):
        """
        Disconnect all databases concurrently.
        """
        tasks = [database.disconnect() for database in self.databases.values()]
        await asyncio.gather(*tasks)


# Load environment variables from the .env file
multi_database: Optional[MultiDatabase] = MultiDatabase(settings.postgres_uris_dict)


async def init_database():
    await multi_database.init()


@contextmanager
def get_session(db_name: str):
    """
    Define a dependency to create a database session asynchronously.

    Returns:
        Database: A NamedTuple with engine and conn attributes for the database connection.
        None: If there was an error connecting to the database.
    """
    # Ensure database is initialized before getting a session
    if multi_database is None:
        init_database()

    with multi_database.get_session(db_name) as session:
        try:
            yield session
        finally:
            session.close()
