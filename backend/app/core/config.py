
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
    
    FIRST_SUPERUSER=str
    FIRST_SUPERUSER_USERNAME=str
    FIRST_SUPERUSER_PASSWORD=str

settings = Settings()