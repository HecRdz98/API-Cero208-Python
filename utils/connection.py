import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


class Database():
    def __init__(self, database_name:str):
        self.db_database = database_name
        self.db_host = os.getenv("DB_HOST")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASS")
        self.db_port = os.getenv("DB_PORT")
        self.engine = self.create_engine_db()


    def create_engine_db(self):
        url = f"mysql+mysqlconnector://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_database}"
        # url = f"mysql+asyncmy://{db_user}:{db_password}@{db_host}:{db_port}/{db_database}"
        engine = create_engine(url)
        return engine
