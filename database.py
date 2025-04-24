from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    def __init__(self):
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        
        self.DATABASE_URL = f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        self.engine: AsyncEngine = None
        self.SessionLocal = None
        self.Base = declarative_base()

    def connect(self):
        self.engine = create_async_engine(self.DATABASE_URL)
        self.SessionLocal = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()

    async def get_db(self):
        async with self.SessionLocal() as session:
            yield session

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

# Instancia única de la base de datos
database = Database()
Base = database.Base
get_db = database.get_db