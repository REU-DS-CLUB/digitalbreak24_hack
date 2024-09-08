import os

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DATABASE")
DB_USER = os.environ.get("POSTGRES_USERNAME")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

BOT_TOKEN = os.environ.get("BOT_TOKEN")

YANDEXGPT_KEY = os.environ.get("YANDEXGPT_KEY")
HUGGINGFACE_KEY = os.environ.get("HUGGINGFACE_KEY")
API_GIGACHAT = os.environ.get("API_GIGACHAT")