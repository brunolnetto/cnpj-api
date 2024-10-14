from typing import Dict
from contextlib import contextmanager

from contextlib import contextmanager
from urllib.parse import urlparse
from psycopg2 import OperationalError
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import pool, text, inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.engine.url import make_url

from backend.app.setup.config import settings


class BaseDatabase:
    def get_session(self):
        raise NotImplementedError()

    def create_database(self):
        raise NotImplementedError()

    def test_connection(self):
        raise NotImplementedError()

    def create_tables(self):
        raise NotImplementedError()

    def print_tables(self):
        raise NotImplementedError()


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

    def get_session(self, db_name):
        """
        Get a session for a specific database.
        """
        if db_name not in self.databases:
            raise ValueError(f"No such database: {db_name}")
        return self.databases[db_name].get_session()

    def create_database(self):
        for name, database in self.databases.items():
            database.create_database()

    def test_connection(self):
        for name, database in self.databases.items():
            database.test_connection()

    def create_tables(self):
        for name, database in self.databases.items():
            database.create_tables()

    def print_tables(self):
        """
        Print the available tables in a specific database.
        """
        for name, database in self.databases.items():
            database.print_tables()

    def init(self):
        for name, database in self.databases.items():
            database.init()

    def disconnect(self):
        for name, database in self.databases.items():
            database.disconnect()


class Database(BaseDatabase):
    """
    This class represents a database connection and session management object.
    It contains two attributes:

    - engine: A callable that represents the database engine.
    - session_maker: A callable that represents the session maker.
    """

    def __init__(self, uri):
        self.uri = uri
        self.base = declarative_base()
        self.engine = create_engine(
            uri,
            poolclass=pool.QueuePool,  # Use connection pooling
            pool_size=20,  # Adjust pool size based on your workload
            max_overflow=10,  # Adjust maximum overflow connections
            # Periodically recycle connections (optional)
            pool_recycle=3600,
        )
        self.session_maker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
    
    def mask_password(self, uri):
        parsed_uri = urlparse(uri)
        userinfo = parsed_uri.username
        password = parsed_uri.password
        masked_password = '*' * len(password) if password else ''
        masked_uri = parsed_uri._replace(netloc=f"{userinfo}:{masked_password}@{parsed_uri.hostname}")
        return masked_uri.geturl()

    @contextmanager
    def get_session(self):
        return self.session_maker()

    def mask_sensitive_data(self) -> str:
        # Parse the URI using SQLAlchemy's make_url
        parsed_uri = make_url(self.uri)

        # Mask the password if it's present
        if parsed_uri.password:
            parsed_uri = parsed_uri.set(password="******")

        # Return the sanitized URI as a string
        return str(parsed_uri)

    def create_database(self):
        masked_uri = self.mask_sensitive_data()
        # Create the database if it does not exist
        try:
            if not database_exists(self.uri):
                # Create the database engine and session maker
                create_database(self.uri)

            print(f"Database {masked_uri} created!")

        except OperationalError as e:
            print(f"Error creating to database {masked_uri}: {e}")

    def test_connection(self):
        masked_uri = self.mask_sensitive_data()
        try:
            with self.engine.connect() as conn:
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

    def init(self):
        """
        Initializes the database connection and creates the tables.

        Args:
            uri (str): The database URI.

        Returns:
            Database: A NamedTuple with engine and conn attributes for the database connection.
            None: If there was an error connecting to the database.
        """

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

    def disconnect(self):
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


# Load environment variables from the .env file
multi_database = None


def create_database_obj():
    global multi_database
    multi_database = MultiDatabase(settings.postgres_uris_dict)


create_database_obj()


def init_database():
    global multi_database
    if not multi_database:
        create_database()

    multi_database.init()

init_database()

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

    session = multi_database.get_session(db_name)
    try:
        yield session
    finally:
        session.close()
