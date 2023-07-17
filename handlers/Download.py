import config, Buttons, Calls, os, Messages

from telebot import types
from bot import FilesDatabase, bot, drive, Users


def Download(message: types.Message):
    import database
    number = message.text
    DBpath = 'Cache/FileCache/' + str(message.chat.id) + '.txt'
    Files = database.DB(DBpath)
    FileTitle = Files.data[number][1]
    FileID = Files.data[number][2]
    FileArgument = Files.data[number][3]
    Destination = Files.data[number][4]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if FileArgument == 'A':
        path = drive.GetFile(
            title=FileTitle, 
            FileID=FileID, 
            folder_path=config.FileCache
            )
        folder = Users.Get(message.chat.id)[-2]
        drive.SendFile(file_path=path, title=FileTitle, folder_parent=str(folder))
        keyboard.add(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
        string = f'Файл {FileTitle} успешно скачан!'
        bot.send_document(chat_id=message.chat.id, document=open(path, 'rb'), caption=string, reply_markup=keyboard)
        os.remove(path)
    else:
        calls = [f'D{number}', f'E{number}', Destination]
        keyboard.add(
            types.InlineKeyboardButton(text=Buttons.download, callback_data=calls[0]),
            types.InlineKeyboardButton(text=Buttons.delete, callback_data=calls[1]),
            types.InlineKeyboardButton(text=Buttons.main, callback_data=calls[2])
        )
        string = f'Что сделать с файлом {FileTitle}?'
        bot.send_message(chat_id=message.chat.id, text=string, reply_markup=keyboard)
        bot.register_callback_query_handler(callback=Actions, func=lambda query: query.data in calls)


def Actions(query: types.CallbackQuery):
    import database
    DBpath = 'Cache/FileCache/' + str(query.message.chat.id) + '.txt'
    Files = database.DB(DBpath)
    number = query.data[1:]
    FileTitle = Files.data[number][1]
    FileID = Files.data[number][2]
    FileArgument = Files.data[number][3]
    Destination = Files.data[number][4]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Destination))
    if query.data[0] == 'D':
        path = drive.GetFile(
            title=FileTitle, 
            FileID=FileID, 
            folder_path=config.FileCache
            )
        keyboard.add(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
        string = f'Файл {FileTitle} успешно скачан!'
        bot.send_document(chat_id=query.message.chat.id, document=open(path, 'rb'), caption=string, reply_markup=keyboard)
    elif query.data[0] == 'E':
        drive.DeleteFile(file_id=FileID)
        keyboard.add(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
        string = f'Файл {FileTitle} успешно удален!'
        bot.send_message(chat_id=query.message.chat.id, text=string, reply_markup=keyboard)
    else:
        import handlers
        handlers.Menu.Menu(query)

