from os import getenv, path, getcwd
from dotenv import load_dotenv
from typing import Dict

from contextlib import contextmanager
from urllib.parse import urlparse
from psycopg2 import OperationalError
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import pool, text, inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

from backend.app.setup.config import settings
from backend.app.setup.logging import logger

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
            db_name: Database(uri)
            for db_name, uri in database_uris.items()
        }
    
    @contextmanager   
    def get_session(self, db_name):
        """
        Get a session for a specific database.
        """
        if db_name not in self.databases:
            raise ValueError(f"No such database: {db_name}")
        
        with self.databases[db_name].get_session() as session:
            yield session

    def create_database(self, db_name):
        for name, database in self.databases.items():
            database.create_database()

    def test_connection(self, db_name):
        for name, database in self.databases.items():
            database.test_connection()

    def create_tables(self):
        for name, database in self.databases.items():
            database.create_tables()

    def print_tables(self, db_name):
        """
        Print the available tables in a specific database.
        """
        for name, database in self.databases.items():
            database.print_tables()
            
    def init(self):
        for name, database in self.databases.items():
            database.init()

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
            poolclass=pool.QueuePool,   # Use connection pooling
            pool_size=20,               # Adjust pool size based on your workload
            max_overflow=10,            # Adjust maximum overflow connections
            pool_recycle=3600,          # Periodically recycle connections (optional)
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
        yield self.session_maker()

    def create_database(self):
        # Create the database if it does not exist
        try:
            if not database_exists(self.uri):
                # Create the database engine and session maker
                create_database(self.uri)

        except OperationalError as e:
            logger.error(f"Error creating to database: {e}")

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                query = text("SELECT 1")

                # Test the connection
                conn.execute(query)

                masked_uri = self.mask_password(self.uri)
                logger.info(f"Connection to the database {masked_uri} established!")

        except OperationalError as e:
            logger.error(f"Error connecting to the database: {e}")

    def create_tables(self):
        """
        Connects to a PostgreSQL database using environment variables for connection details.

        Returns:
            Database: A NamedTuple with engine and conn attributes for the database connection.
            None: If there was an error connecting to the database.

        """
        try:
            # Create all tables defined using the Base class (if not already created)
            self.base.metadata.create_all(self.engine)

        except Exception as e:
            logger.error(f"Error creating tables in the database: {str(e)}")

    def print_tables(self):
        """
        Print the available tables in the database.
        """
        try:
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()
            logger.info(f"Available tables: {tables}")
        except Exception as e:
            logger.error(f"Error fetching table names: {str(e)}")

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
            logger.error(f"Error creating database: {e}")

        try:
            self.test_connection()
        except Exception as e:
            logger.error(f"Error testing connection: {e}")

        try:
            self.create_tables()
        except Exception as e:
            logger.error(f"Error creating tables: {e}")

        try:
            self.print_tables()
        except Exception as e:
            logger.error(f"Error print available tables: {e}")

# Load environment variables from the .env file
multi_database = None

def init_database():
    global multi_database
    multi_database = MultiDatabase(settings.postgres_uris_dict)
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

    with multi_database.get_session(db_name) as session:
        try:
            yield session
        finally:
            session.close()
