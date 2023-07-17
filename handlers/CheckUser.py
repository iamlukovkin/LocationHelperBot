import Calls, Messages, Buttons

from bot import bot
from telebot import types


def CheckUser(query: types.CallbackQuery):
    user = query.message.chat.id
    import database 
    Operations = database.DB('Database/Operation.txt')
    try:
        Operations.Delete(str(user))
    except Exception as e:
        pass
    Operations.AddString(str(user), mass=['CheckUser'])
    import database
    db = database.DB('Database/User.txt')
    if db.Test(user):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
        bot.send_message(chat_id=user, text=Messages.registred, reply_markup=keyboard)
    else:
        keys = database.DB('Database/keys.txt')
        keys.AddString(key='Reg' + str(user), mass=['True'])
        bot.send_message(chat_id=user, text=Messages.not_registred)
        bot.send_message(chat_id=user, text=Messages.enter_username)


def Registration(message: types.Message):
    import database, pyDrive, config
    db = database.DB('Database/User.txt')
    string = str(message.text)
    user = message.chat.id
    drive = pyDrive.GDrive(credentials=config.credentials, scope=config.scope)
    UserFolder = drive.CreateFolder(title=string, parent_folder_id=config.users_folder_id)
    mass = [string, UserFolder['id']]
    for Title in 'Methods', 'Diary':
        folder = drive.CreateFolder(title=Title, parent_folder_id=UserFolder['id'])
        mass.append(folder['id'])
    db.AddString(user, mass)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
    bot.send_message(chat_id=user, text=Messages.complete_reg, reply_markup=keyboard)


def handler():
    bot.register_callback_query_handler(callback=CheckUser, func=lambda querry: querry.data == Calls.CheckUser)