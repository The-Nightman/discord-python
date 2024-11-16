
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        # top level .env file
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"

    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_PORT: int = 5432
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str = ""
    TEST_POSTGRES_DB: str = ""

    def TEST_SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.TEST_POSTGRES_USER,
            password=self.TEST_POSTGRES_PASSWORD,
            host=self.TEST_POSTGRES_SERVER,
            port=self.TEST_POSTGRES_PORT,
            path=self.TEST_POSTGRES_DB,
        )

    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str

    # LOGGING_ENABLED is initially fetched as a string, convert it to a boolean using lambda if in List
    LOGGING_ENABLED: bool = property(
        lambda self: self.LOGGING_ENABLED.lower() in ["true", "1"])
    LOGGING_LEVEL: str = "INFO"


settings = Settings()
