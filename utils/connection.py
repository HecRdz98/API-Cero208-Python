import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_engine = os.getenv("DB_ENGINE")
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_database = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")


def create_engine_db():
    url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    # url = f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
    engine = create_engine(url)
    return engine

engine = create_engine_db()