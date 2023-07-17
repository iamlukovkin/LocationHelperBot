import telebot
import config
import Calls
import Messages
import Buttons

from telebot import types
from bot import bot


def Menu(query: types.CallbackQuery):
    string = Messages.choose_action
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(text=Buttons.methods, callback_data=Calls.Methods),
        types.InlineKeyboardButton(text=Buttons.diary, callback_data=Calls.Diary),
        types.InlineKeyboardButton(text=Buttons.HelpNavigation, callback_data=Calls.Help)
    )
    bot.send_message(
        chat_id=query.message.chat.id,
        text=string,
        reply_markup=keyboard
    )


def Methods(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(text=Buttons.SearchAdmin, callback_data=Calls.SearchAdmin),
        types.InlineKeyboardButton(text=Buttons.UserLibrary, callback_data=Calls.UserLibrary),
        types.InlineKeyboardButton(text=Buttons.UserUpload, callback_data=Calls.UserUpload),
        types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Menu)
    )
    bot.send_message(chat_id=query.message.chat.id, text=Messages.choose_action, reply_markup=keyboard)


def HelpInfo(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Menu))
    bot.send_message(chat_id=query.message.chat.id, text=Messages.HelpInfo, reply_markup=keyboard)


def handler():
    bot.register_callback_query_handler(callback=Menu, func=lambda query: query.data == Calls.Menu)
    bot.register_callback_query_handler(callback=Methods, func=lambda query: query.data == Calls.Methods)
    bot.register_callback_query_handler(callback=HelpInfo, func=lambda query: query.data == Calls.Help)