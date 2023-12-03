from aiogram import Dispatcher, Bot

from .local_settings import API_TOKEN
    

dp = Dispatcher()
bot = Bot(token=API_TOKEN, parse_mode="HTML")

async def launch_bot():
    await dp.start_polling(bot)
