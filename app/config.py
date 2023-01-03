from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "todo-app"
    DEBUG_MODE: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DB_URL: str = ""
    DB_NAME: str = ""


settings = Settings()
