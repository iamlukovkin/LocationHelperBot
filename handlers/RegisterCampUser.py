import Buttons, Calls, Messages, config, database

from telebot import types
from bot import bot, FilesDatabase
from pyDrive import GDrive


def RegisterUser(query: types.CallbackQuery):
    user = query.message.chat.id
    keys = database.DB('Database/keys.txt')
    keys.AddString(key='CampReg' + str(query.message.chat.id), mass=['True'])
    bot.send_message(chat_id=user, text='Пришлите пароль')
    bot.register_message_handler(callback=CreateUserCamp, func=lambda message: True, pass_bot=True)


def CreateUserCamp(message: types.Message):
    user = message.chat.id
    PasswordsDatabase = database.DB('Database/Passwords.txt')
    CampDatabsse = database.DB('Database/Camp.txt')
    keys = database.DB('Database/keys.txt')
    if keys.Get('CampReg' + str(message.chat.id))[-1] == 'True':
        if str(message.text) in PasswordsDatabase.data.keys():
            CampDatabsse.AddString(key=user, mass=PasswordsDatabase.Get(key=str(user)))
            text = 'Регистарция в лагерной смене прошла успшено!'
        else:
            text = 'Пароль неверный!'
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Menu))
        bot.send_message(chat_id=user, text=text, reply_markup=keyboard)
        keys.Delete('CampReg' + str(message.chat.id))
        keys.AddString(key='CampReg' + str(message.chat.id), mass=['False'])
