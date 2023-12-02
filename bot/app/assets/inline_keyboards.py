from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


# menu_buttons
methods_button = InlineKeyboardButton(text='Методические указания📚', callback_data='methods')
diary_button = InlineKeyboardButton(text='Педагогический дневник📖', callback_data='diary')
help_button = InlineKeyboardButton(text='Помощь по навигацииℹ️', callback_data='help')
menu_buttons = [[methods_button], [diary_button], [help_button]]


# rsreu_site_button = InlineKeyboardButton(text='Сайт РГРТУ', url='http://rsreu.ru/')
# cdo_site_button = InlineKeyboardButton(text='Сайт CDO', url='http://cdo.rsreu.ru/')
# edu_site_button = InlineKeyboardButton(text='Сайт EDU', url='http://edu.rsreu.ru/')
# menu_button = InlineKeyboardButton(text='В главное меню', callback_data='goto_menu')
