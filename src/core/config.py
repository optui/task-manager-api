from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./data/task_manager.db"
    api_title: str = "Task Manager API"
    api_version: str = "1.0"
    api_description: str = "A RESTful API for managing tasks"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
