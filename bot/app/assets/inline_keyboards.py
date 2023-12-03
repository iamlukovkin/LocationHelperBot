from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup


# menu_buttons
methods_button = InlineKeyboardButton(text='📚', callback_data='methods')
diary_button = InlineKeyboardButton(text='📖', callback_data='diary')
help_button = InlineKeyboardButton(text='ℹ️', callback_data='help')
profile_button = InlineKeyboardButton(text='👤', callback_data='profile')
menu_buttons = [[methods_button, diary_button, help_button, profile_button]]


# methods buttons
new_document_button = InlineKeyboardButton(text='🔍', callback_data='new_document')
library_button = InlineKeyboardButton(text='📔', callback_data='library')
upload_button = InlineKeyboardButton(text='📄', callback_data='upload')
main_button = InlineKeyboardButton(text='📍', callback_data='main')
methods_buttons = [[new_document_button, library_button, upload_button, main_button]]
delete_button = InlineKeyboardButton(text='🗑', callback_data='delete')