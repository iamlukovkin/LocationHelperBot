import telebot
import config

from pyDrive import GDrive
from database import DB

bot = telebot.TeleBot(token = config.main_bot_token)
drive = GDrive(credentials=config.credentials, scope=config.scope)
FilesDatabase = DB(config.Files)
Users = DB(config.UserDatabase)
Camp = DB(config.DiaryDatabase)
AdminBot = telebot.TeleBot(token=config.admin_bot_token)