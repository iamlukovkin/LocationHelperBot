from aiogram.types import WebAppInfo

from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import KeyboardButton


hello_button = KeyboardButton(text='Начнём! 📍')
menu_button = KeyboardButton(text='Главное меню 📍')

register_button = KeyboardButton(
    text='Зарегистрироваться📝', 
    web_app=WebAppInfo(url='https://iamlukovkin.github.io/LocationHelperBot/site/webapp/registration.html')
)
