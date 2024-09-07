from psycopg import connect
from psycopg.rows import dict_row
import os

from .vault import Settings

settings = Settings()


def get_connection():

    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    dbname = os.getenv("POSTGRES_DATABASE")
    user = os.getenv("POSTGRES_USERNAME")
    password = os.getenv("POSTGRES_PASSWORD")

    cnn = connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        row_factory=dict_row
    )

    return cnn
