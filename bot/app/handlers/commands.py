from aiogram.filters import Command
from aiogram import types

from .. import assets
from ..database.requests import get_user

from ..bot_app import dp


@dp.message(Command(commands='start'))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [assets.reply_keyboards.hello_button]
        ], 
        resize_keyboard=True
    )
    message_text = assets.message_text.start_message
    await get_user(message.from_user.id, message.from_user.username, message.from_user.full_name)
    await message.answer(text=message_text, reply_markup=keyboard)
    return