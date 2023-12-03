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
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    
    def __init__(self, telegram_id: int, username: str = None, fullname: str = None):
        self.telegram_id = telegram_id
        self.username = username
        self.fullname = fullname
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


class Profile(Base):
    __tablename__ = 'profiles'

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    profile_name: Mapped[str] = mapped_column(String)
    job_title: Mapped[str] = mapped_column(String)
    bio: Mapped[str] = mapped_column(String)
    google_folder_id: Mapped[str] = mapped_column(String, nullable=True)
    
    
    def __init__(self, telegram_id: int, profile_name: str, job_title: str, bio: str, google_folder_id: str = None):
        self.telegram_id = telegram_id
        self.profile_name = profile_name
        self.job_title = job_title
        self.bio = bio
        self.google_folder_id = google_folder_id


async def conn_to_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
