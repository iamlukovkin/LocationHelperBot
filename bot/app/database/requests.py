from .models import User, async_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


# get or create user by telegram_id
async def get_user(telegram_id: int, username: str, full_name: str) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if not user:
            user = User(telegram_id=telegram_id, username=username, fullname=full_name)
            session.add(user)
            await session.commit()
        return user
        

async def add_user(user: int, username: str, fullname: str) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user))
        if result.scalar() is None:
            user = User(telegram_id=user, username=username, fullname=fullname)
            session.add(user)
            await session.commit()
            return False
        else:
            return True
