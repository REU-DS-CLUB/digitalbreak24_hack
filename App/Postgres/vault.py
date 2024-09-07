from pydantic_settings import BaseSettings
import utils.config as config


class Settings(BaseSettings):

    pg_host: str = config.DB_HOST
    pg_port: str = config.DB_PORT
    pg_database: str = config.DB_NAME
    pg_user: str = config.DB_USER
    pg_password: str = config.DB_PASS
