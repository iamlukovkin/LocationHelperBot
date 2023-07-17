import Buttons, Calls, Messages

from telebot import types
from bot import bot


def Start(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.doContinue, callback_data=Calls.CheckUser))
    bot.send_message(chat_id=message.chat.id, text=Messages.Start, reply_markup=keyboard)


def Help(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Menu))
    bot.send_message(chat_id=message.chat.id, text=Messages.HelpInfo)


def handler():
    bot.register_message_handler(callback=Start, commands=['start'])
    bot.register_message_handler(callback=Help, commands=['help'])
    bot.register_callback_query_handler(callback=Help, func=lambda querry: querry == Calls.Help)