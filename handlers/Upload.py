import config, Buttons, Calls, os, Messages

from telebot import types
from bot import FilesDatabase, bot, drive, Users, Camp


def Awaiting(query: types.CallbackQuery):
    import database
    user = query.message.chat.id
    Operations = database.DB('Database/Operation.txt')
    Operations.Delete(str(user))
    Operations.AddString(str(user), mass=['Uploading'])
    global destination, call
    if query.data == Calls.UserUpload:
        destination = Users.Get(query.message.chat.id)[-2]
        call = Calls.Methods
    else:
        destination = Camp.Get(query.message.chat.id)[-2]
        call = Calls.Diary
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=call))
    bot.send_message(chat_id=query.message.chat.id, text=Messages.send_doc, reply_markup=keyboard)
    bot.register_message_handler(callback=Uploading, content_types=['document', 'photo', 'audio', 'video', 'voice'])


def Uploading(message):
    file_name = message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    path = config.FileCache + '/' + file_name
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    drive.SendFile(file_path=path, title=file_name, folder_parent=destination)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        types.InlineKeyboardButton(text=Buttons.back, callback_data=call),
        types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu)
    )
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Файл {file_name} успешно загружен на сервер!',
        reply_markup=keyboard
    )
    os.remove(path)


def handler():
    bot.register_callback_query_handler(
        callback=Awaiting, 
        func=lambda query: query.data == Calls.UserUpload or query.data == Calls.DiaryUpload
        )
    