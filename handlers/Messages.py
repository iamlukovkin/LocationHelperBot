import Buttons, Calls, Messages, config, database

from telebot import types
from bot import bot, FilesDatabase
from pyDrive import GDrive
import handlers


def Message(message: types.Message):
    user = message.chat.id
    import database 
    Operations = database.DB('Database/Operation.txt')
    operation = Operations.data[str(user)][-1]
    if operation == 'Diary':
        handlers.AdminAndUserLib.CheckPassword(message)
    elif operation == 'CheckUser':
        handlers.CheckUser.Registration(message)
    elif operation == 'EditQuestion':
        handlers.CreateDoc.SaveAnswer(message)
    elif operation == 'Files':
        handlers.Download.Download(message)
    elif operation == 'Uploading':
        handlers.Upload.Uploading(message)
    else:
        Operations.Delete(str(user))
        Operations.AddString(key=str(user), mass=['Waiting'])
    

def handler():
    bot.register_message_handler(callback=Message, func=lambda message: True)
