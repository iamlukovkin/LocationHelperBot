import os
import shutil
import datetime
import logging
import time
import base64
import httplib2
import requests

import telebot as tb

from telebot import types
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
from common import ButtonsText
from common import AnswerText

def pyDrive():
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('locationbot-389713-571b4d9edd7a.json', scope)
    gauth.Authorize()
    drive = GoogleDrive(gauth)
    return drive


drive = pyDrive()
chat_api = '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'
TOKEN = '6048732407:AAEGRA6prdW1ymtjLamIvn53_vDh_IyQ5yE'
ADMIN_TOKEN = '5974126919:AAEURflwb8Gmqzy_iEhp4Gy3DqF6wxgE_Ks'


bot = tb.TeleBot(token = TOKEN)
ab = tb.TeleBot(token = ADMIN_TOKEN)

methods_id = '1gXDbDUoYDfI6cFhwbIrq35SpOZCyYhxm'

cache_data = {}
del_cache = {}
adm_cache = {}

PD_log = {
    'Year': '',
    'Camp': '',
    'Squad': ''
}

PD_data = {
    'Year': [],
    'Camp': [],
    'Squad': []
}

questions = {
    'Q1': 'Дата заполнения',
    'Q2': 'Название дня',
    'Q3': 'Цели дня',
    'Q4': 'План на день',
    'Q5': 'Анализ дня, выводы, размышления',
    'Q6': 'Имя и фамилия автора записи'
}

answers = {
    'Q1': 'Пусто',
    'Q2': 'Пусто',
    'Q3': 'Пусто',
    'Q4': 'Пусто',
    'Q5': 'Пусто',
    'Q6': 'Пусто'
}


def check_folder(folder_id):
    drive = pyDrive()
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    return file_list


def check_user(user_id, param):
    ans = None
    if param == 'user_name':
        search = 1
    elif param == 'folder_id':
        search = 2
    elif param == 'methods_folder_id':
        search = 3
    elif param == 'diary_folder_id':
        search = 4
    with open('Admin/DB.txt', 'r') as f:
        for line in f:
            line = line.strip()
            parts = line.split(":")
            for i in range(0, len(parts)):
                if parts[0] == str(user_id):
                    ans = parts[search].strip() if search != 1 else parts[search]
    return ans


@bot.callback_query_handler(func=lambda call: call.data in cache_data.keys())
def accept_file(call):
    global cache_data
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    id = call.message.chat.id
    txt = f'Что сделать с файлом "{call.data}"?'
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(
            text=ButtonsText.download,
            callback_data=f'DOWN{call.data}'
            ),
        types.InlineKeyboardButton(
            text=ButtonsText.delete,
            callback_data=f'DELE{call.data}'
            )
    )
    bot.send_message(
        chat_id=id,
        text=txt,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data[:4] =='DOWN')
def get_file_usr(call):
    drive = pyDrive()
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    global cache_data
    file_name = call.data[4:]
    data = cache_data[file_name]
    parts = data.split(':')
    dir_id = parts[0]
    file_id = parts[1]
    chat_id = parts[2]
    func = parts[3]
    list_files = check_folder(dir_id)
    for file in list_files:
        dir = f"Cache/{file['title']}"
        if file_id == file['id']:
            file = drive.CreateFile({'id': file_id})
            file.GetContentFile(dir)
            if dir[-4:] == '.jpg':
                bot.send_photo(
                    chat_id=chat_id,
                    photo = open(dir, 'rb')
                    )
            else:
                bot.send_document(
                    chat_id=chat_id,
                    document=open(dir, 'rb')
                    )
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.row(
                types.InlineKeyboardButton(
                    text=ButtonsText.back,
                    callback_data=func
                    ),
                types.InlineKeyboardButton(
                    text=ButtonsText.main,
                    callback_data='main'
                    )
                )
            bot.send_message(
                chat_id=chat_id,
                text=f'Файл {file["title"]} успешно скачан!',
                reply_markup=markup
                )
            os.remove(dir)


@bot.callback_query_handler(func=lambda call: call.data in adm_cache.keys())
def get_file_adm(call):
    drive = pyDrive()
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    global adm_cache
    file_name = call.data
    data = adm_cache[file_name]
    parts = data.split(':')
    dir_id = parts[0]
    file_id = parts[1]
    chat_id = parts[2]
    func = parts[3]
    list_files = check_folder(dir_id)
    for file in list_files:
        dir = f"Cache/{file['title']}"
        if file_id == file['id']:
            file = drive.CreateFile({'id': file_id})
            file.GetContentFile(dir)
            with open(dir, 'rb') as f:
                folder_id = check_user(
                    user_id=chat_id,
                    param="methods_folder_id"
                    )
                file_title = file['title']
                file_metadata = {'title': file_title}
                if folder_id:
                    file_metadata['parents'] = [{'id': folder_id}]
                file = drive.CreateFile(file_metadata)
                file.SetContentFile(dir)
                file.Upload()
                bot.send_document(
                    chat_id=chat_id,
                    document=f
                    )
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.row(
                    types.InlineKeyboardButton(
                        text=ButtonsText.back,
                        callback_data=func
                        ),
                    types.InlineKeyboardButton(
                        text=ButtonsText.main,
                        callback_data='main'
                        )
                )
                bot.send_message(
                    chat_id=chat_id,
                    text=f'Файл {file["title"]} успешно скачан!',
                    reply_markup = markup
                    )
            os.remove(dir)


@bot.callback_query_handler(func=lambda call: call.data[:4] =='DELE')
def delete_file(call):
    drive = pyDrive()
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    global cache_data
    file_name = call.data[4:]
    data = cache_data[file_name]
    parts = data.split(':')
    file_id = parts[1]
    id = parts[2]
    func = parts[3]
    file = drive.CreateFile({'id': file_id})
    file.Delete()
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(
            text=ButtonsText.back,
            callback_data=func
            ),
        types.InlineKeyboardButton(
            text=ButtonsText.main,
            callback_data='main'
            )
    )
    bot.send_message(
        chat_id=id,
        text="Успешно!",
        reply_markup=markup
        )


@bot.message_handler(commands=['start'])
def do_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
    markup.add(types.KeyboardButton(text='Погнали!'))

    bot.send_message(
        chat_id = message.chat.id,
        text = f'Привет!\nТы находишься на главной странице '
        f'бота Локация.Помощник📍\nЭтот бот поможет тебе '
        f'упростить работу в смене.\n'
        f'Давай скорее же начнем!🤓',
        reply_markup = markup)


@bot.message_handler(func=lambda message: message.text == 'Погнали!')
def auth(message):
    if check_user(
        user_id=message.chat.id,
        param='user_name'
        ) == None:
        bot.send_message(
            chat_id=message.chat.id,
            text='Кажется, на платформе ты впервые. Давай пройдем простую регистрацию!'
            )
        first_name(message)
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text='Кажется, ты уже зарегистрирован! Приступим к работе!'
            )
        help_button(message)


def first_name(message):
    id = message.chat.id
    txt = 'Введи имя и фамилию'
    bot.send_message(
        chat_id=id,
        text=txt
        )
    bot.register_next_step_handler(
        message=message,
        callback=complete_reg
        )


def complete_reg(message):
    drive = pyDrive()
    parent_folder = '1s_nzGkAUE4_vVZEbrgAcom1pzd1CtVoc'     # Users

    folder_metadata = {
        'title': f'{message.text}',     #Folder of user
        'parents':[{'id': parent_folder}],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    main_folder = drive.CreateFile(folder_metadata)
    main_folder.Upload()

    folder_metadata = {
        'title': f'{"Methods"}',    #Methods folder of user
        'parents':[{'id': main_folder["id"]}],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder1 = drive.CreateFile(folder_metadata)
    folder1.Upload()

    folder_metadata = {
        'title': f'{"Diary"}',      #Diary folder of user
        'parents':[{'id': main_folder["id"]}],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder2 = drive.CreateFile(folder_metadata)
    folder2.Upload()

    with open('Admin/DB.txt', 'r') as f:
        text = f.read()

    with open('Admin/DB.txt', 'w') as f:
        text += f'{message.chat.id}: {message.text}: {main_folder["id"]}: {folder1["id"]}: {folder2["id"]}\n'
        f.write(text)

    bot.send_message(
        chat_id=message.chat.id,
        text='Регистрация прошла успешно!'
    )


    ab_markup = types.InlineKeyboardMarkup(row_width=2)
    ab_markup.row(
        types.InlineKeyboardButton(
            text='Оставить',
            callback_data='leave_user'
            ),
        types.InlineKeyboardButton(
            text='Заблокировать',
            callback_data=f'DELUS_{message.chat.id}'
            )
    )

    ab.send_message(
        chat_id = message.chat.id,
        text=f'Зарегистрирован новый пользователь: {message.text}.',
        reply_markup=ab_markup
    )

    help_button(message)


@ab.callback_query_handler(func=lambda call: call.data == 'leave_user')
def leave_user(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )


def help_button(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)

    markup.add(types.KeyboardButton(ButtonsText.main))

    bot.send_message(
        chat_id = message.chat.id,
        text=f'Ты в любой момент можешь вернуться в начало.\n'
        f'Достаточно нажать на кнопку\n'
        f'{ButtonsText.main} внизу',
        reply_markup = markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'main')
def go_to_main(call):
    do_main(call.message)


@bot.message_handler(func=lambda message: message.text == 'Главное меню📍')
def do_main(message):
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            text=ButtonsText.methods,
            callback_data='methods'
            ),

        types.InlineKeyboardButton(
            text=ButtonsText.diary,
            callback_data='choose_year'
            ),

        types.InlineKeyboardButton(
                text=ButtonsText.HelpNavigation,
                callback_data='help_navigation'
                )
    )
    bot.send_message(
        chat_id = message.chat.id,
        text = 'Выбери действие: ',
        reply_markup = markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'methods')
def methods(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.search_admin,
            callback_data = 'admin_methods'
            ),

        types.InlineKeyboardButton(
                text = ButtonsText.library,
                callback_data = 'library'
                ),

        types.InlineKeyboardButton(
            text = ButtonsText.upload,
            callback_data = 'upload'
            ),

        types.InlineKeyboardButton(
            text = ButtonsText.main,
            callback_data = 'main'
            )
        )
    bot.send_message(
        chat_id = call.message.chat.id,
        text = 'Выбери действие: ',
        reply_markup = markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'admin_methods')
def admin_methods(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    folder = '1gXDbDUoYDfI6cFhwbIrq35SpOZCyYhxm'
    user_id = call.message.chat.id
    list_files = check_folder(folder)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        call_data = f'{folder}:{file["id"]}:{user_id}:admin_methods'
        adm_cache[file['title']] = call_data
        markup.add(
            types.InlineKeyboardButton(
                text=file['title'],
                callback_data=file['title']
                )
            )
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.back,
            callback_data = 'methods'
            ),

        types.InlineKeyboardButton(
            text = ButtonsText.main,
            callback_data = 'main'
            )
        )
    txt = 'Выберите файл'
    bot.send_message(
        chat_id=user_id,
        text=txt,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'library')
def library(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    folder = check_user(call.message.chat.id, 'methods_folder_id')
    user_id = call.message.chat.id
    list_files = check_folder(folder)
    markup = types.InlineKeyboardMarkup(row_width=1)
    if len(list_files) != 0:
        for file in list_files:
            call_data = f'{folder}:{file["id"]}:{user_id}:library'
            cache_data[file['title']] = call_data
            markup.add(
                types.InlineKeyboardButton(
                    text=file['title'],
                    callback_data=file['title']
                    ),
            )
        markup.add(
            types.InlineKeyboardButton(
                text = ButtonsText.back,
                callback_data = 'methods'
                ),

            types.InlineKeyboardButton(
                text = ButtonsText.main,
                callback_data = 'main'
                )
        )
        txt = 'Выберите файл'
        bot.send_message(
            chat_id=call.message.chat.id,
            text=txt,
            reply_markup=markup
            )

    else:
        txt = 'На данный момент в этой папке пусто, но ты можешь загрузить свой документ или добавить файлы от методистов.'
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                text = ButtonsText.search_admin,
                callback_data = 'admin_methods'
                ),

            types.InlineKeyboardButton(
                text = ButtonsText.upload,
                callback_data = 'upload'
                ),

            types.InlineKeyboardButton(
                text = ButtonsText.main,
                callback_data = 'main'
                )
            )
        bot.send_message(
            chat_id = call.message.chat.id,
            text = txt,
            reply_markup = markup
            )


@bot.callback_query_handler(func=lambda call: call.data == 'upload')
def upload(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    bot.send_message(
        chat_id=call.message.chat.id,
        text='Пришлите документ'
        )
    bot.register_next_step_handler(
        message=call.message,
        callback=g_upload
        )


def g_upload(message):
    drive = pyDrive()
    if message.document is not None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'))

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        path = f'Cache/{message.document.file_name}'
        file_title = message.document.file_name
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.photo[-1] is not None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                text = ButtonsText.main,
                callback_data = 'main'
                )
            )

        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
        try:
            file_title = photo.file_name
        except Exception as e:
            file_title = 'img.jpg'
        path = f'Cache/{file_title}'
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)

    folder_id = check_user(
        user_id=message.chat.id,
        param="methods_folder_id"
        )
    file_metadata = {'title': file_title}
    if folder_id:
        file_metadata['parents'] = [{'id': folder_id}]
    file = drive.CreateFile(file_metadata)
    file.SetContentFile(path)
    file.Upload()
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Файл {file_title} успешно загружен!',
        reply_markup=markup
        )
    os.remove(path)


@bot.callback_query_handler(func=lambda call: call.data == 'main')
def main(call):
    do_main(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'choose_year')
def choose_year(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    list_files = check_folder('1GKxxMDjrkuO40Xlt97oKdoEZa9ErFdGW')
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        PD_data['Year'] = file['id']
        markup.add(
            types.InlineKeyboardButton(
                text=file['title'],
                callback_data=file['id']
                )
        )
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.main,
            callback_data = 'main'
            )
        )
    txt = 'Выберите год📅'
    bot.send_message(
        chat_id=call.message.chat.id,
        text=txt,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data in PD_data['Year'])
def choose_camp(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    PD_log['Year'] = call.data
    list_files = check_folder(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        PD_data['Camp'].append(file['id'])
        markup.add(
            types.InlineKeyboardButton(
                text=file['title'],
                callback_data=file['id']
                )
        )
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.main,
            callback_data = 'main'
            ),
        types.InlineKeyboardButton(
            text = ButtonsText.ChooseYear,
            callback_data = 'choose_year'
            )
    )
    txt = 'Выберите смену⛳'
    bot.send_message(
        chat_id=call.message.chat.id,
        text=txt,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data in PD_data['Camp'])
def squad(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    PD_log['Camp'] = call.data
    list_files = check_folder(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        PD_data['Squad'].append(file['id'])
        markup.add(
            types.InlineKeyboardButton(
                text=file['title'],
                callback_data=file['id']
                )
            )
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.ChooseYear,
            callback_data = 'choose_year'
            ),
        types.InlineKeyboardButton(
            text = ButtonsText.ChooseCamp,
            callback_data = f'{PD_log["Year"]}'
            )
        )
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.main,
            callback_data = 'main'
            )
        )
    txt = 'Выберите отряд🫂'
    bot.send_message(
        chat_id=call.message.chat.id,
        text=txt,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data in PD_data['Squad'])
def choose_file(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    PD_log['Squad'] = call.data

    user_id = call.message.chat.id
    folder = call.data
    list_files = check_folder(folder)
    markup = types.InlineKeyboardMarkup(row_width=5)
    markup_row = []
    if len(list_files) != 0:
        txt = 'Выберите файл\n'
        for i in range(0, len(list_files)):
            call_data = f'{folder}:{list_files[i]["id"]}:{user_id}:{folder}'
            cache_data[list_files[i]['title']] = call_data
            txt += f'{i+1} - {list_files[i]["title"]}\n'
            markup_row.append(
                types.InlineKeyboardButton(
                    text=f'{i + 1}',
                    callback_data=list_files[i]['title']
                    )
            )
            if len(markup_row) == 5:
                markup.row(*markup_row)
                markup_row = []
        if len(markup_row) != 0:
            markup.row(*markup_row)
    else:
        txt = 'Пока что здесь нет записей, но есть возможность загрузить свои файлы или создать новую запись прямо здесь!'
    markup.row(
        types.InlineKeyboardButton(
            text = ButtonsText.CreateFile,
            callback_data = 'create_PD'
            )
        )
    markup.row(
        types.InlineKeyboardButton(
            text = ButtonsText.UploadFile,
            callback_data = 'upload_PD'
            )
        )
    markup.row(
        types.InlineKeyboardButton(
            text = ButtonsText.main,
            callback_data = 'main'
            )
        )
    markup.row(
        types.InlineKeyboardButton(
            text = ButtonsText.ChooseYear,
            callback_data = 'choose_year'
            )
        )
    markup.row(types.InlineKeyboardButton(
        text = ButtonsText.ChooseCamp,
        callback_data = f'{PD_log["Year"]}'
            )
        )
    markup.row(
        types.InlineKeyboardButton(
            text = ButtonsText.ChooseSquad,
            callback_data = f'{PD_log["Camp"]}'
            )
        )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=txt,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'upload_PD')
def upload(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    bot.send_message(
        call.message.chat.id,
        'Пришлите документ'
        )
    bot.register_next_step_handler(
        call.message,
        PD_upload
        )


def PD_upload(message):
    drive = pyDrive()
    bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
    if message.document is not None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                text = ButtonsText.main,
                callback_data = 'main'
                ),
            types.InlineKeyboardButton(
                text = ButtonsText.back,
                callback_data = f'{PD_log["Squad"]}'
                )
            )
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        path = f'Cache/{message.document.file_name}'
        file_title = message.document.file_name
        with open(path, 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.photo[-1] is not None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                text = ButtonsText.main,
                callback_data = 'main'
                )
            )

        photo = message.photo[-1]
        file_id = photo.file_id
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
        try:
            file_title = photo.file_name
        except Exception as e:
            file_title = 'img.jpg'
        path = f'Cache/{file_title}'
        response = requests.get(file_url)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                file.write(response.content)

    folder_id = PD_log['Squad']

    file_metadata = {'title': file_title}
    if folder_id:
        file_metadata['parents'] = [{'id': folder_id}]

    file = drive.CreateFile(file_metadata)
    file.SetContentFile(path)
    file.Upload()
    bot.send_message(
        message.chat.id,
        text=f'Файл {file_title} успешно загружен!',
        reply_markup=markup
        )
    os.remove(path)


@bot.callback_query_handler(func=lambda call: call.data == 'create_PD')
def new_note(call):
    global answers
    answers = {
        'Q1': 'Пусто',
        'Q2': 'Пусто',
        'Q3': 'Пусто',
        'Q4': 'Пусто',
        'Q5': 'Пусто',
        'Q6': 'Пусто'
    }
    create_PD(call)


def JUMP_create(call):
    create_PD(call.message)


@bot.callback_query_handler(func=lambda call: call.data == 'doc_now')
def create_PD(call):
    id = call.message.chat.id
    text = f'''
    '''

    message_text = f'''
1 - изменить "{questions['Q1']}"
2 - изменить "{questions['Q2']}"
3 - изменить "{questions['Q3']}"
4 - изменить "{questions['Q4']}"
5 - изменить "{questions['Q5']}"
6 - изменить "{questions['Q6']}"
🗄 - Сохранить документ
📁 - Вернуться к списку файлов
❔ - Правила заполнения
    '''
    markup = types.InlineKeyboardMarkup(row_width=5)
    markup.row(
        types.InlineKeyboardButton(
            text='1', callback_data='Q1'
        ),
        types.InlineKeyboardButton(
            text='2', callback_data='Q2'
        ),
        types.InlineKeyboardButton(
            text='3', callback_data='Q3'
        ),
        types.InlineKeyboardButton(
            text='4', callback_data='Q4'
        ),
        types.InlineKeyboardButton(
            text='5', callback_data='Q5'
        ),
        types.InlineKeyboardButton(
            text='6', callback_data='Q6'
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            text='🗄', callback_data='save_doc'
    ),
        types.InlineKeyboardButton(
            text='📁', callback_data=f'{PD_log["Squad"]}'
    ),
        types.InlineKeyboardButton(
            text='❔', callback_data='rules_PD'
    ))
    dir = 'Admin/План анализа.jpg'
    bot.send_photo(
        chat_id=id,
        photo = open(dir, 'rb'),
        caption = text

    )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=message_text,
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data in questions.keys())
def edit_note(call):
    id = call.message.chat.id
    global ans_now
    ans_now = call.data
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='Оставить предыдущий ответ', callback_data='doc_now'))
    bot.send_message(
        chat_id=id,
        text=f'Ответ на данный момент:\n"{answers[ans_now]}"'
        )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=f'Введите ответ на пункт "{questions[ans_now]}"',
        reply_markup=markup
        )
    bot.register_next_step_handler(
        message=call.message,
        callback=save_ans
        )


def save_ans(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.row(
        types.InlineKeyboardButton(
            text='В начало🗄', callback_data='doc_now'
    ))
    answers[ans_now] = message.text
    bot.send_message(
        chat_id=message.chat.id,
        text='Ответ сохранен',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data == 'rules_PD')
def rules_PD(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text = ButtonsText.doContinue, callback_data = 'PD_note'),
        types.InlineKeyboardButton(text = ButtonsText.back, callback_data = f'{PD_log["Squad"]}')
        )

    text = AnswerText.RulesPD
    bot.send_message(
        chat_id=call.message.chat.id,
        text=text,
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data =='save_doc')
def naming(call):
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.message_id
        )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=AnswerText.TypeNameDoc
    )
    bot.register_next_step_handler(
        message=call.message,
        callback=saving)


def paragraph_add(
        doc,
        text: str,
        heading: bool
        ):
    paragraph = doc.add_paragraph(
        text,
        style = 'heading1' if heading else 'normal'
        )
    paragraph_format = paragraph.paragraph_format
    paragraph_format.left_indent = Inches(0.49)
    paragraph_format.line_spacing = 1.5


def saving(message):
    drive = pyDrive()
    global document
    document = Document()

    heading1 = document.styles.add_style(
            'heading1', WD_STYLE_TYPE.PARAGRAPH
        )
    heading1.base_style = document.styles['Normal']
    font = heading1.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    font.bold = True

    normal = document.styles.add_style(
            'normal', WD_STYLE_TYPE.PARAGRAPH
        )
    font = normal.font
    font.name = 'Times New Roman'
    font.size = Pt(14)
    font.bold = False

    for quest in questions.keys():
        paragraph_add(
            doc=document,
            text=questions[quest],
            heading=True
            )
        paragraph_add(
            doc=document,
            text=answers[quest],
            heading=False
            )
    file_title = f'{message.text}.docx'
    document.save(f'Cache/{file_title}')

    path = f'Cache/{file_title}'
    folder_id = PD_log['Squad']
    file_metadata = {'title': file_title}
    if folder_id:
        file_metadata['parents'] = [{'id': folder_id}]
    file = drive.CreateFile(file_metadata)
    file.SetContentFile(path)
    file.Upload()
    os.remove(path)

    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(
            text=ButtonsText.main,
            callback_data = 'main'
            ),
        types.InlineKeyboardButton(
            text=ButtonsText.back,
            callback_data = f'{PD_log["Squad"]}'
            )
    )
    bot.send_message(
        chat_id = message.chat.id,
        text = f'Файл {file_title} успешно сохранен!',
        reply_markup=markup
        )


    ab.send_message(
        chat_id = message.chat.id,
        text = f'Пользователь {check_user(message.chat.id, "user_name")} отправил файл {file_title}',
        reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == 'help_navigation')
def help_navigation(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width = 1)
    markup.add(
        types.InlineKeyboardButton(
            text = ButtonsText.main, 
            callback_data = 'main'
        )
    )

    info_text = AnswerText.HelpInfo
    bot.send_message(
        chat_id = call.message.chat.id,
        text = info_text,
        reply_markup = markup
        )


if __name__ == '__main__':
    bot.polling(non_stop = True)