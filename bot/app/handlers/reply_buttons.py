from aiogram import types, Router
from aiogram.filters import Filter

from .. import assets
from ..bot_app import dp


router = Router(name=__name__)

class MyFilter(Filter):
    def __init__(self, my_text: str) -> None:
        self.my_text = my_text
        
    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.my_text


@dp.message(MyFilter(assets.reply_keyboards.hello_button.text))
async def cmd_hello(message: types.Message):
    from app.assets.inline_keyboards import menu_buttons
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=menu_buttons
    )
    await message.answer(text=assets.message_text.start_message, reply_markup=keyboard)

