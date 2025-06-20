from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
        'env_ignore_empty': True,
        'extra': 'ignore',
    }

    ALLOWED_HOST: list[str] = []

    DATABASE_NAME: str = 'postgres'

    DATABASE_USER: str = 'postgres'
    DATABASE_PASSWORD: str | None = None

    DATABASE_HOST: str = 'localhost'
    DATABASE_PORT: int = 5432

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:  # noqa: N802
        return PostgresDsn.build(
            scheme='postgresql+asyncpg',
            username=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
            port=self.DATABASE_PORT,
            path=self.DATABASE_NAME,
        )

    QUERY_LOGGER: bool = False


settings = Settings()
