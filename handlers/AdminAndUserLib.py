import Buttons, Calls, Messages, config, database

from telebot import types
from bot import bot, FilesDatabase
from pyDrive import GDrive


def CreateUserCamp(message: types.Message):
    user = message.chat.id
    PasswordsDatabase = database.DB('Database/Passwords.txt')
    CampDatabsse = database.DB('Database/Camp.txt')
    if str(message.text) in PasswordsDatabase.data.keys():
        CampDatabsse.AddString(key=user, mass=PasswordsDatabase.Get(key=str(user)))
        text = 'Регистарция прошла успшено!'
    else:
        text = 'Пароль неверный!'
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.ShowDiary))
    bot.send_message(chat_id=user, text=text, reply_markup=keyboard)


def ShowDocuments(query: types.CallbackQuery):
    user = query.message.chat.id
    import database 
    Operations = database.DB('Database/Operation.txt')
    Operations.Delete(str(user))
    Operations.AddString(str(user), mass=['Files'])

    drive = GDrive(credentials=config.credentials, scope=config.scope)
    if query.data == Calls.UserLibrary:
        db = database.DB(path=config.UserDatabase)
        FolderID = db.Get(key=str(query.message.chat.id))[-2]
    elif query.data == Calls.Diary:
        DiaryDB = database.DB(path=config.DiaryDatabase)
        FolderID = '1j8AdatUICPl8Tgqgiworixr0_FaIsLHR'
    else:
        FolderID = config.methods_folder
    folder = drive.GetFromFolder(FolderID)
    keyboard = types.InlineKeyboardMarkup(row_width=5)
    if len(folder) != 0:
        DBpath = 'Cache/FileCache/' + str(query.message.chat.id) + '.txt'
        with open(DBpath, 'w+') as file:
            file.write('')
            Files = database.DB(DBpath)
        if query.data == Calls.ShowDiary:
            db = database.DB(path=config.DiaryDatabase)
            string = f'Ваш отряд: {db.Get(query.message.chat.id)[-1]}\n{Messages.choose_file}\n'
        FILEstring = ''
        StringsMass = []
        for file in folder:
            index = folder.index(file) + 1
            FILEstring += f'\n{index} - {file["title"]}'
            if query.data == Calls.SearchAdmin:
                QueryArg = 'A'
            else:
                QueryArg = 'U'
            Files.AddString(key=str(folder.index(file) + 1), mass=[file['title'], file['id'], QueryArg, query.data])
            if len(FILEstring) > 2000:
                StringsMass.append(FILEstring)
                FILEstring = ''
        if len(FILEstring) != 0:
            StringsMass.append(FILEstring)
        if query.data == Calls.SearchAdmin or query.data == Calls.UserLibrary:
            keyboard.row(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Methods))
        else:
            keyboard.row(types.InlineKeyboardButton(text=Buttons.CreateFile, callback_data=Calls.CreateFile))
            keyboard.row(types.InlineKeyboardButton(text=Buttons.UploadFile, callback_data=Calls.DiaryUpload))
        keyboard.row(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
        string = 'Введите номер необходимого документа'
        for ItemString in StringsMass:
            bot.send_message(chat_id=query.message.chat.id, text=ItemString)
    else:
        if query.data == Calls.SearchAdmin:
            string = Messages.MethodsEmpty
            keyboard.row(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Methods))
            keyboard.row(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
        elif query.data == Calls.UserLibrary:
            keyboard.row(types.InlineKeyboardButton(text=Buttons.UserUpload, callback_data=Calls.UserUpload))
            keyboard.row(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Methods))
            keyboard.row(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
            string = Messages.folder_is_empty
        else:
            db = database.DB(path=config.DiaryDatabase)
            string = f'Ваш отряд: {db.Get(query.message.chat.id)[-1]}\n{Messages.no_files}\n'
            keyboard.row(types.InlineKeyboardButton(text=Buttons.UploadFile, callback_data=Calls.DiaryUpload))
            keyboard.row(types.InlineKeyboardButton(text=Buttons.CreateFile, callback_data=Calls.CreateFile))
            keyboard.row(types.InlineKeyboardButton(text=Buttons.main, callback_data=Calls.Menu))
    bot.send_message(chat_id=query.message.chat.id, text=string, reply_markup=keyboard)

        
def Diary(query: types.CallbackQuery):
    user = query.message.chat.id
    Operations = database.DB('Database/Operation.txt')
    Operations.Delete(str(user))
    Operations.AddString(str(user), mass=['Diary'])
    DiaryDB = database.DB(path=config.DiaryDatabase)
    CampDB = database.DB('Database/Camp.txt')
    if str(user) not in DiaryDB.data.keys():
        bot.send_message(chat_id=user, text='Пришлите пароль')
    else:
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton(text=Buttons.Yes, callback_data=Calls.ShowDiary))
        keyboard.add(types.InlineKeyboardButton(text=Buttons.No, callback_data='EditCampList'))
        keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Menu))
        bot.send_message(chat_id=user, text=f'Ваш отряд - {CampDB.Get(str(user))[-1]}?', reply_markup=keyboard)


def CheckPassword(message: types.Message):
    user = message.chat.id
    Passwords = database.DB('Database/Passwords.txt')
    CampDB = database.DB('Database/Camp.txt')
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if message.text in Passwords.data.keys():
        keyboard.add(types.InlineKeyboardButton(text=Buttons.doContinue, callback_data=Calls.ShowDiary))
        CampDB.AddString(key=str(user), mass=Passwords.Get(str(message.text)))
        string = 'Успешно!'
    else:
        keyboard.add(types.InlineKeyboardButton(text=Buttons.back, callback_data=Calls.Menu))
        string = 'Пароль неверный!'
    bot.send_message(chat_id=user, text=string, reply_markup=keyboard)


def DeleteUser(query: types.CallbackQuery):
    CampDB = database.DB('Database/Camp.txt')
    CampDB.Delete(key=str(query.message.chat.id))
    Diary(query)


def handler():
    bot.register_callback_query_handler(
        callback=ShowDocuments, 
        func=lambda query: query.data == Calls.SearchAdmin or query.data == Calls.UserLibrary or query.data == Calls.ShowDiary
    )
    bot.register_callback_query_handler(callback=ShowDocuments, func=lambda query: query.data == Calls.Diary)
    bot.register_callback_query_handler(callback=DeleteUser, func=lambda query: query.data == 'EditCampList')
