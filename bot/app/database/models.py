from typing import Any
from sqlalchemy import Boolean
from sqlalchemy import BigInteger
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from ..local_settings import SQL_ALCHEMY_URL
from sqlalchemy import String

engine = create_async_engine(SQL_ALCHEMY_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    google_folder_id: Mapped[str] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    def __repr__(self):
        return f'<User(telegram_id={self.telegram_id}, username={self.username}, fullname={self.fullname}, google_folder_id={self.google_folder_id})>'
    
    def __str__(self):
        return f'<User(telegram_id={self.telegram_id}, username={self.username}, fullname={self.fullname}, google_folder_id={self.google_folder_id})>'
    
    def __hash__(self):
        return self.telegram_id
    
    def __eq__(self, other):
        return self.telegram_id == other
    
    def __lt__(self, other):
        return self.telegram_id < other
    
    def __gt__(self, other):
        return self.telegram_id > other
    
    def __init__(self, telegram_id: int, username: str = None, fullname: str = None, google_folder_id: str = None):
        self.telegram_id = telegram_id
        self.username = username
        self.fullname = fullname
        self.google_folder_id = google_folder_id
        self.is_admin = False


class File(Base):
    __tablename__ = 'files'

    filename: Mapped[str] = mapped_column(String)
    file_id: Mapped[str] = mapped_column(String, primary_key=True)
    parent_folder_id: Mapped[str] = mapped_column(String)
    
    telegram_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    
    def __init__(self, file_id: str, filename: str, parent_folder_id: str, telegram_id: int = None):
        self.filename = filename
        self.file_id = file_id
        self.parent_folder_id = parent_folder_id
        self.telegram_id = telegram_id




async def conn_to_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
