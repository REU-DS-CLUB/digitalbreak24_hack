from poetry import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DATABASE")
DB_USER = os.environ.get("POSTGRES_USERNAME")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
