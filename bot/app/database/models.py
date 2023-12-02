from sqlalchemy import Boolean
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

from ..local_settings import SQL_ALCHEMY_URL
from sqlalchemy import String

engine = create_async_engine(SQL_ALCHEMY_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String(50))
    def __repr__(self):
        return f"User(telegram_id={self.telegram_id}, username={self.username}, fullname={self.fullname})"
    def __str__(self):
        return f"User(telegram_id={self.telegram_id}, username={self.username}, fullname={self.fullname})"
    def __eq__(self, other):
        return self.telegram_id == other.telegram_id
    def __hash__(self):
        return hash(self.telegram_id)
    def __ne__(self, other):
        pass
    

async def conn_to_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
