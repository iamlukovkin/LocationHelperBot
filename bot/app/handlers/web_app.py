from aiogram import types, Router
from aiogram.filters import Filter

from ..bot_app import dp
from .. import assets

router = Router(name=__name__)

class MyFilter(Filter):
    def __init__(self, check_data: str) -> None:
        self.check_data = check_data
        
    async def __call__(self, message: types.Message) -> bool:
        import json
        data = json.loads(message.web_app_data.data)
        return self.check_data == data['action']


@dp.message(MyFilter(check_data="registration_profile"))
async def document_request(message: types.Message):
    await message.answer(
        text='<b>📝Идет регистрация!</b>\nПожалуйста, немного подождите...',
        reply_markup=types.ReplyKeyboardRemove()
    )
    import json
    data = json.loads(message.web_app_data.data)
    profile_name = data['question_1']
    job_title = data['question_2']
    bio = data['question_3']
    
    from ..modules.pyDrive import GDrive
    from ..local_settings import credentials, scope, users_folder_id
    drive = GDrive(credentials, scope)
    folder_id = drive.CreateFolder(title=profile_name, parent_folder_id=users_folder_id)
    folder_id = folder_id['id']
    
    from ..database.requests import add_profile
    await add_profile(
        telegram_id=message.from_user.id,
        profile_name=profile_name,
        job_title=job_title,
        bio=bio,
        google_folder_id=folder_id
    )
    await message.answer(
        text=assets.message_text.success_registration_message,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    assets.inline_keyboards.main_button,
                    assets.inline_keyboards.profile_button
                ]
            ]
        )
    )


@dp.message(MyFilter(check_data="edit_profile"))
async def document_request(message: types.Message):
    await message.answer(
        text='<b>📝 Вносим изменения!</b>\nПожалуйста, немного подождите...',
        reply_markup=types.ReplyKeyboardRemove()
    )
    import json
    data = json.loads(message.web_app_data.data)
    profile_name = data['question_1']
    job_title = data['question_2']
    bio = data['question_3']
    
    from ..database.requests import get_profile, add_profile, delete_profile
    profile = await get_profile(message.from_user.id)
    fodler_id = profile.google_folder_id
    delete_profile(message.from_user.id)
    await add_profile(
        telegram_id=message.from_user.id,
        profile_name=profile_name,
        job_title=job_title,
        bio=bio,
        google_folder_id=fodler_id
    )
    from .callbacks import cmd_profile
    await cmd_profile(message)
    
