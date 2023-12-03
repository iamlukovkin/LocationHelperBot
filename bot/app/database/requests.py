from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .models import async_session
from .models import User
from .models import File
from .models import Profile


async def get_user(telegram_id: int, username: str, full_name: str) -> User:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()
        if not user:
            user = User(telegram_id=telegram_id, username=username, fullname=full_name)
            session.add(user)
            await session.commit()
        return user


# refresh database from google drive files
async def refresh_db():
    print('Refreshing database...')
    
    # delete all rows from table
    async with async_session() as session:
        await session.execute(File.__table__.delete())
        await session.commit()
    print('Database cleared')
    
    # get files from google drive
    from ..local_settings import credentials, scope, methods_folder
    from ..modules.pyDrive import conn_google_drive
    drive = await conn_google_drive(credentials, scope)
    files = drive.GetFromFolder(methods_folder)
    print(f'Found {len(files)} files')
    
    # add files to database
    async with async_session() as session:
        for file in files:
            try:
                session.add(
                    File(
                        filename=file['title'],
                        file_id=file['id'], 
                        parent_folder_id=file['parents'][0]['id']
                    )
                )
            except IntegrityError:
                pass
        await session.commit()
    print('Database refreshed')


async def get_files_from_methods():
    from ..local_settings import methods_folder
    
    async with async_session() as session:
        result = await session.execute(select(File).where(File.parent_folder_id == methods_folder))
        files = result.scalars().all()
        return files
    
    
async def get_files(telegram_id: int = None):
    async with async_session() as session:
        if not telegram_id:
            # get all rows
            result = await session.execute(select(File))
        else:
            result = await session.execute(select(File).where(File.telegram_id == telegram_id))
        files = result.scalars().all()
        return files


async def get_file(file_id, telegram_id: int = None):
    async with async_session() as session:
        if not telegram_id:
            result = await session.execute(select(File).where(File.file_id == file_id))
        else:
            result = await session.execute(select(File).where(File.file_id == file_id, File.telegram_id == telegram_id))
        file = result.scalar()
        return file
    

async def add_file(file_id: str, filename: str, parent_folder_id: str, telegram_id: int = None):
    async with async_session() as session:
        file = File(
            filename=filename, 
            file_id=file_id, 
            parent_folder_id=parent_folder_id, 
            telegram_id=telegram_id
        )
        session.add(file)
        await session.commit()


async def delete_file(file_id, telegram_id):
    async with async_session() as session:
        await session.execute(File.__table__.delete().where(File.file_id == file_id, File.telegram_id == telegram_id))
        await session.commit()

# get profile from database by telegram_id
async def get_profile(telegram_id):
    async with async_session() as session:
        result = await session.execute(select(Profile).where(Profile.telegram_id == telegram_id))
        profile = result.scalar()
        return profile


async def add_profile(telegram_id: int, profile_name: str, job_title: str, bio: str, google_folder_id: str = None):
    async with async_session() as session:
        profile = Profile(
            telegram_id=telegram_id, 
            profile_name=profile_name, 
            job_title=job_title, 
            bio=bio, 
            google_folder_id=google_folder_id
        )
        session.add(profile)
        await session.commit()


async def delete_profile(telegram_id):
    async with async_session() as session:
        await session.execute(Profile.__table__.delete().where(Profile.telegram_id == telegram_id))
        await session.commit()
        

async def edit_profile(telegram_id: int, profile_name: str, job_title: str, bio: str):
    async with async_session() as session:
        await session.execute(
            Profile.__table__.update()
            .where(Profile.telegram_id == telegram_id)
            .values(profile_name=profile_name, job_title=job_title, bio=bio)
        )
        await session.commit()