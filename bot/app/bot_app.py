from aiogram import Dispatcher, Bot

from .local_settings import API_TOKEN
    
    
dp = Dispatcher()

async def launch_bot():
    bot = Bot(token=API_TOKEN, parse_mode="HTML")
    await dp.start_polling(bot)
