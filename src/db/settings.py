from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DATABASE_URL: str = (
        "postgresql://postgres:567234@localhost:5432/my_postgres_task_08"
    )

    class Config:
        env_file = ".env"  # Allows overriding via a .env file


settings = Settings()
