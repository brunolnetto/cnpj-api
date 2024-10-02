from datetime import timedelta
from warnings import warn
import platform

from typing import Optional, Dict, Literal, List, Any, Union

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

from pydantic import (
    Field,
    AnyUrl,
    BeforeValidator,
    computed_field,
    model_validator,
    field_validator,
    ValidationInfo,
)


from typing_extensions import Self, Annotated
import toml

DEFAULT_PASSWORD = "postgres"
POSTGRES_DSN_SCHEME = "postgresql+asyncpg"
BASE_URI_TEMPLATE = "{dsn_scheme}://{user}:{password}@{host}:{port}/{database}"


def generate_db_uri(dsn_scheme, user, password, host, port, database):
    """
    Generate a database URI using a template.

    Args:
        user (str): The database user.
        password (str): The database password.
        host (str): The database host.
        port (int): The database port.
        database (str): The database name.

    Returns:
        str: The generated database URI.
    """
    return BASE_URI_TEMPLATE.format(
        dsn_scheme=dsn_scheme,
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def parse_comma_separated(v: Any) -> Union[List[str], str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]

    if isinstance(v, (list, str)):
        return v

    raise ValueError(v)


# Project settings
with open("pyproject.toml", "r", encoding="utf8") as f:
    config = toml.load(f)


# Settings class
class Settings(BaseSettings):
    """App settings."""

    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    VERSION: str = config["tool"]["poetry"]["version"]
    PROJECT_NAME: str = config["tool"]["poetry"]["name"]
    DESCRIPTION: str = config["tool"]["poetry"]["description"]
    API_V1_STR: str = "/api"

    ENVIRONMENT: Literal["development", "production"] = "development"
    MACHINE_NAME: str = platform.node()
    SIGNATURE: str = "Suas Vendas rocks!"

    DOMAIN: str = "localhost:8000"

    # CORS
    BACKEND_CORS_ORIGINS: Annotated[
        Union[List[AnyUrl], str], BeforeValidator(parse_comma_separated)
    ] = []

    # 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1 * 24 * 60

    # Page size
    PAGE_SIZE: int = 10

    @computed_field  # type: ignore[misc]
    @property
    def server_host(self) -> str:
        # Use HTTPS for anything other than local development
        protocol = "http" if self.ENVIRONMENT == "development" else "https"
        return f"{protocol}://{self.DOMAIN}"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"

    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    POSTGRES_DBNAME_RFB: str = ""
    POSTGRES_DBNAME_AUDIT: str = ""

    DEFAULT_RATE_LIMIT: str
    DEFAULT_BURST_RATE_LIMIT: str
    DEFAULT_RATE_LIMITS: List[str] = Field(default_factory=list)

    # Define cron parameters for task logs cleanup
    CLEANUP_CRON_KWARGS: Dict[str, str] = {
        "minute": "0",
        "hour": "0",  # Runs at midnight
        "day": "*",  # Every first day of the month
        "month": "*",  # Every month
        "day_of_week": "*",  # Every day of the week
    }

    IP_LOOKUP_CRON_KWARGS: Dict[str, str] = {
        "minute": "0",
        "hour": "*/2",  # Runs every 2 hours
        "day": "*",  # Every first day of the month
        "month": "*",  # Every month
        "day_of_week": "*",  # Every day of the week
    }

    # Define the age of request logs to be cleaned up
    REQUEST_CLEANUP_AGE: Dict[str, Any] = {"days": 30}

    # Define the age of task logs to be cleaned up
    TASK_CLEANUP_AGE: timedelta = timedelta(days=30)

    # Define the age of task logs to be cleaned up
    DEBUG_CLEANUP_AGE: timedelta = timedelta(days=14)

    # Define the maximum number of rows to retain
    CLEANUP_MAX_ROWS: int = 10**6

    @field_validator("DEFAULT_RATE_LIMITS", mode="before")
    @classmethod
    def default_rate_limits(cls, v: Optional[str], values: ValidationInfo) -> List[str]:
        rate_limit = values.data.get("DEFAULT_RATE_LIMIT")
        burst_rate_limit = values.data.get("DEFAULT_BURST_RATE_LIMIT")
        return [rate_limit, burst_rate_limit]

    def _check_default_secret(self, var_name: str, value: Union[str, None]) -> None:
        if value == DEFAULT_PASSWORD:
            message = (
                f'The value of {var_name} is "{DEFAULT_PASSWORD}", '
                "for security, please change it, at least for deployments."
            )
            if self.ENVIRONMENT == "development":
                warn(message, stacklevel=1)
            else:
                raise ValueError(message)

    @computed_field
    @property
    def postgres_uris_dict(self) -> str:
        return {
            db_name: generate_db_uri(
                POSTGRES_DSN_SCHEME,
                self.POSTGRES_USER,
                self.POSTGRES_PASSWORD,
                self.POSTGRES_HOST,
                self.POSTGRES_PORT,
                db_name,
            )
            for db_name in [self.POSTGRES_DBNAME_RFB, self.POSTGRES_DBNAME_AUDIT]
        }

    @model_validator(mode="after")
    def _enforce_non_default_secrets(self) -> Self:
        self._check_default_secret("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)

        return self


settings = Settings()
