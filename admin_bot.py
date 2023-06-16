import os
import shutil
import datetime
import logging
import time

import telebot as tb

from telebot import types
from pathlib import Path
from docx import Document
from docx.shared import Pt
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.style import WD_STYLE_TYPE
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive


def pyDrive():
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('locationbot-389713-571b4d9edd7a.json', scope)
    gauth.Authorize()
    drive = GoogleDrive(gauth)
    return drive


chat_api = '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'
TOKEN = '6048732407:AAEGRA6prdW1ymtjLamIvn53_vDh_IyQ5yE'
ADMIN_TOKEN = '5974126919:AAEURflwb8Gmqzy_iEhp4Gy3DqF6wxgE_Ks'

us_bot = tb.TeleBot(token = TOKEN)
bot = tb.TeleBot(token = ADMIN_TOKEN)

methods_id = '1gXDbDUoYDfI6cFhwbIrq35SpOZCyYhxm'

cache_data = {}
del_cache = {}
adm_cache = {}

cache_message = ''

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

pwd = 'Location_is_my_love'


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
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    id = call.message.chat.id
    txt = f'Что сделать с файлом "{call.data}"?'
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(text='Скачать⬇️', callback_data=f'DOWN{call.data}'),
        types.InlineKeyboardButton(text='Удалить🗑', callback_data=f'DELE{call.data}')
    )
    bot.send_message(chat_id=id, text=txt, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data[:4] =='DOWN')
def get_file_usr(call):
    drive = pyDrive()
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
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
            bot.send_document(chat_id=chat_id, document=open(dir, 'rb'))
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.row(
                types.InlineKeyboardButton(text='Назад🔄', callback_data=func),
                types.InlineKeyboardButton(text='Главное меню📍', callback_data='main')
            )
            bot.send_message(chat_id=chat_id, text=f'Файл {file["title"]} успешно скачан!', reply_markup = markup)
            os.remove(dir)


@bot.callback_query_handler(func=lambda call: call.data[:4] =='DELE')
def delete_file(call):
    drive = pyDrive()
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
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
        types.InlineKeyboardButton(text='Назад🔄', callback_data=func),
        types.InlineKeyboardButton(text='Главное меню📍', callback_data='main')
    )
    bot.send_message(chat_id=id, text="Успешно!", reply_markup=markup)


@bot.message_handler(commands=['start'])
def auth(message):
    bot.send_message(chat_id=message.chat.id, text='Введите пароль')
    bot.register_next_step_handler(message, check_pwd)


def check_pwd(message):
    if message.text == pwd:
        bot.delete_message(chat_id = message.chat.id, message_id = message.message_id)
        hello(message)
    else:
        bot.send_message(message.chat.id, 'Неверный пароль!')
        auth(message)
    

def hello(message):
    id = message.chat.id
    text = '''
Приветствую! Это ознакомительная часть бота Локация.Управление🕹️
С его помощью ты сможешь:
- Ознакомиться с педагогическими дневниками вожатых,
- Загрузить новые методические материалы
- Сделать объявление, которое будет доступно всем владельцам бота Локация.Помощник📍
- Ни в коем случае не передавай никому этот пароль, иначе все узнают о твоих фотографиях басиков в личной папке!

Важно: это общий бот для ВСЕХ методистов. У всех общая база документов. На все личное есть @LocationHelperBot
Удачи!❤️
'''
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='Главное меню🕹️', callback_data='main')
    )
    bot.send_message(chat_id=id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'main')
def do_main(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='Методические указания📚', callback_data='methods'),

        types.InlineKeyboardButton(text='Педагогический дневник📖', callback_data='choose_year'),

        types.InlineKeyboardButton(text='Сделать объявление⚠️', callback_data='alert')
    )
    bot.send_message(chat_id = call.message.chat.id, text = 'Выбери действие: ', reply_markup = markup)


@bot.callback_query_handler(func=lambda call: call.data == 'methods')
def admin_methods(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    folder = '1gXDbDUoYDfI6cFhwbIrq35SpOZCyYhxm'
    user_id = call.message.chat.id
    list_files = check_folder(folder)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        call_data = f'{folder}:{file["id"]}:{user_id}:methods'
        cache_data[file['title']] = call_data
        markup.add(
            types.InlineKeyboardButton(text=file['title'], callback_data=file['title'])
        )
    markup.add(      
        types.InlineKeyboardButton(text = 'Назад🔄', callback_data = 'methods'),
        types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'),
        types.InlineKeyboardButton(text = 'Загрузить документ📄', callback_data = 'load')
    )
    txt = 'Выберите файл'
    bot.send_message(chat_id=user_id, text=txt, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'load')
def upload(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    bot.send_message(call.message.chat.id, 'Пришлите документ')
    bot.register_next_step_handler(call.message, g_upload)


def g_upload(message):
    drive = pyDrive()
    if message.document is not None:
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'))
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    path = f'Admin_cache/{message.document.file_name}'
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    folder_id = '1gXDbDUoYDfI6cFhwbIrq35SpOZCyYhxm'
    file_title = message.document.file_name
    file_metadata = {'title': file_title}
    if folder_id:
        file_metadata['parents'] = [{'id': folder_id}]

    file = drive.CreateFile(file_metadata)
    file.SetContentFile(path)
    file.Upload()
    bot.send_message(message.chat.id, text=f'Файл {file_title} успешно загружен!', reply_markup=markup)
    os.remove(path)
        

@bot.callback_query_handler(func=lambda call: call.data == 'choose_year')
def choose_year(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    folder ='1GKxxMDjrkuO40Xlt97oKdoEZa9ErFdGW'
    list_files = check_folder(folder)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        PD_data['Year'] = file['id']
        markup.add(
            types.InlineKeyboardButton(text=file['title'], callback_data=file['id'])
        )
    markup.add(
        types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main')
        )
    txt = 'Выберите год📅'
    bot.send_message(chat_id=call.message.chat.id, text=txt, reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: call.data in PD_data['Year'])
def choose_camp(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    PD_log['Year'] = call.data
    list_files = check_folder(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        PD_data['Camp'].append(file['id'])
        markup.add(
            types.InlineKeyboardButton(text=file['title'], callback_data=file['id'])
        )
    markup.add(
        types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'),
        types.InlineKeyboardButton(text = 'Выбрать другой год📅', callback_data = 'choose_year')
    )
    txt = 'Выберите смену⛳'
    bot.send_message(chat_id=call.message.chat.id, text=txt, reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: call.data in PD_data['Camp'])
def squad(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
    PD_log['Camp'] = call.data
    list_files = check_folder(call.data)
    markup = types.InlineKeyboardMarkup(row_width=1)
    for file in list_files:
        PD_data['Squad'].append(file['id'])
        markup.add(
            types.InlineKeyboardButton(text=file['title'], callback_data=file['id'])
        )
    markup.add(
        types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'),
        types.InlineKeyboardButton(text = 'Выбрать другой год📅', callback_data = 'choose_year'),
        types.InlineKeyboardButton(text = 'Выбрать другую смену⛳', callback_data = f'{PD_log["Year"]}')
        )
    txt = 'Выберите отряд🫂'
    bot.send_message(chat_id=call.message.chat.id, text=txt, reply_markup=markup)
    

@bot.callback_query_handler(func=lambda call: call.data in PD_data['Squad'])
def choose_file(call):
    bot.delete_message(chat_id = call.message.chat.id, message_id = call.message.message_id)
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
                types.InlineKeyboardButton(text=f'{i + 1}', callback_data=list_files[i]['title'])
            )
            if len(markup_row) == 5:
                markup.row(*markup_row)
                markup_row = []
        if len(markup_row) != 0:
            markup.row(*markup_row)
    else:
        txt = 'Пока что здесь нет записей, но есть возможность загрузить свои файлы или создать новую запись прямо здесь!'
    markup.row(types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'))
    markup.row(types.InlineKeyboardButton(text = 'Выбрать другой год📅', callback_data = 'choose_year'))
    markup.row(types.InlineKeyboardButton(text = 'Выбрать другую смену⛳', callback_data = f'{PD_log["Year"]}'))
    markup.row(types.InlineKeyboardButton(text = 'Выбрать другой отряд🫂', callback_data = f'{PD_log["Camp"]}'))
    bot.send_message(chat_id=call.message.chat.id, text=txt, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'alert')
def alert(call):
    bot.send_message(call.message.chat.id, text='Пришлите текст объявления')
    bot.register_next_step_handler(call.message, sending)



def get_users():
    mass = []
    with open('Admin/DB.txt', 'r') as f:
        for line in f:
            line = line.strip()
            parts = line.split(":")
            mass.append(parts[0])
    return mass

mass = get_users()

def sending(message):
    markup = types.InlineKeyboardMarkup(row_width=5)
    markup.row(types.InlineKeyboardButton(text = 'Главное меню📍', callback_data = 'main'))
    for user in get_users():
        us_bot.send_message(
            chat_id = user,
            text = f'Новое сообщение от руководителя!\n\n{message.text}',
            reply_markup=markup
        )
    
    bot.send_message(
        chat_id=message.chat.id,
        text = 'Готово!',
        reply_markup=markup
    ),



def handle_photo(message):
    drive = pyDrive()
    photo_dst = f'Admin_cache/'
    file_id = message.photo[-1].file_id
    file = bot.get_file(file_id)
    file_name = file.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file.file_path)

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    shutil.move(file_name, f'{photo_dst}photo.jpg')



if __name__ == '__main__':
    bot.polling(non_stop = True)
