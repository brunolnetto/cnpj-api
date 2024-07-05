from os import getenv, path, getcwd
from dotenv import load_dotenv
from psycopg2 import OperationalError
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import pool, text, inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


from backend.app.setup.logging import logger
from backend.app.database.schemas import Base

class Database:
    """
    This class represents a database connection and session management object.
    It contains two attributes:

    - engine: A callable that represents the database engine.
    - session_maker: A callable that represents the session maker.
    """

    def __init__(self, uri):
        self.uri = uri
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

                logger.info("Connection to the database established!")

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
            Base.metadata.create_all(self.engine)

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


def get_db_uri():
    env_path = path.join(getcwd(), ".env")
    load_dotenv(env_path)

    # Get environment variables
    host = getenv("POSTGRES_HOST", "localhost")
    port = int(getenv("POSTGRES_PORT", "5432"))
    user = getenv("POSTGRES_USER", "postgres")
    passw = getenv("POSTGRES_PASSWORD", "postgres")
    database_name = getenv("POSTGRES_DBNAME")

    # Connect to the database
    return f"postgresql://{user}:{passw}@{host}:{port}/{database_name}"


# Load environment variables from the .env file
database = None

def init_database():
    global database
    uri = get_db_uri()

    database = Database(uri)
    database.init()


async def get_db():
    """
    Define a dependency to create a database connection

    Returns:
        Database: A NamedTuple with engine and conn attributes for the database connection.
        None: If there was an error connecting to the database.
    """

    uri = get_db_uri()

    database = Database(uri)
    database.init()

    yield database


async def get_session():
    """
    Define a dependency to create a database session asynchronously.

    Returns:
        Database: A NamedTuple with engine and conn attributes for the database connection.
        None: If there was an error connecting to the database.
    """
    # Ensure database is initialized before getting a session
    if database is None:
        init_database()

    with database.session_maker() as session:
        try:
            yield session
        finally:
            session.close()
