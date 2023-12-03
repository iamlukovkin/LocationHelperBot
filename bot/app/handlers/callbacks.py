from aiogram import types, Router
from aiogram.filters import Filter

from .. import assets

from ..bot_app import dp

router = Router(name=__name__)

class MyFilter(Filter):
    def __init__(self, my_query: str) -> None:
        self.my_query = my_query
        
    async def __call__(self, query: types.CallbackQuery) -> bool:
        return query.data == self.my_query


class DocIDFilter(Filter):
    def __init__(self, my_query: str) -> None:
        self.my_query = my_query
        
    async def __call__(self, query: types.CallbackQuery) -> bool:
        from ..database.requests import get_files
        files = await get_files()
        for file in files:
            if file.file_id == query.data:
                return True


# main menu
@dp.callback_query(MyFilter(assets.inline_keyboards.main_button.callback_data))
async def cmd_main(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=assets.message_text.menu_message,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=assets.inline_keyboards.menu_buttons
        )
    )
    await callback_query.answer()


# methods menu
@dp.callback_query(MyFilter(assets.inline_keyboards.methods_button.callback_data))
async def cmd_methods(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        text=assets.message_text.methods_message,
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=assets.inline_keyboards.methods_buttons
        )
    )
    await callback_query.answer()


# new document
@dp.callback_query(MyFilter(assets.inline_keyboards.new_document_button.callback_data))
async def cmd_new_document(callback_query: types.CallbackQuery):
    message_text = assets.message_text.new_document_message
    
    from ..database.requests import get_files_from_methods
    files = await get_files_from_methods()
    counter = 0
    buttons_row = []
    buttons = []
    while counter < len(files):
        message_text += f'{counter + 1} - {files[counter].filename}\n'
        buttons_row.append(
            types.InlineKeyboardButton(
                text=str(counter + 1),
                callback_data=files[counter].file_id
            )
        )
        if len(buttons_row) == 5:
            buttons.append(buttons_row)
            buttons_row = []
        counter += 1
    if len(buttons_row) != 5:
        buttons.append(buttons_row)
    
    buttons.append([assets.inline_keyboards.main_button, assets.inline_keyboards.methods_button])
    message_text += "\n" + assets.message_text.main_menu_vector
    message_text += "\n" + assets.message_text.methods_menu_vector
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.callback_query(MyFilter(assets.inline_keyboards.library_button.callback_data))
async def cmd_library(callback_query: types.CallbackQuery):
    message_text = assets.message_text.library_message
    
    from ..database.requests import get_files
    files = await get_files(callback_query.from_user.id)
    counter = 0
    buttons_row = []
    buttons = []
    if len(files) == 0:
        message_text += "У вас ещё нет ни одного документа\n"
    while counter < len(files):
        message_text += f'{counter + 1} - {files[counter].filename}\n'
        buttons_row.append(
            types.InlineKeyboardButton(
                text=str(counter + 1),
                callback_data=files[counter].file_id
            )
        )
        if len(buttons_row) == 5:
            buttons.append(buttons_row)
            buttons_row = []
        counter += 1
    if len(buttons_row) != 5:
        buttons.append(buttons_row)
    
    buttons.append(
        [
            assets.inline_keyboards.main_button, 
            assets.inline_keyboards.methods_button, 
            assets.inline_keyboards.delete_button
        ]
    )
    message_text += "\n" + assets.message_text.main_menu_vector
    message_text += "\n" + assets.message_text.methods_menu_vector
    message_text += "\n" + assets.message_text.delete_button_vector
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )
    await callback_query.answer()


@dp.callback_query(MyFilter(assets.inline_keyboards.delete_button.callback_data))
async def cmd_delete(callback_query: types.CallbackQuery):
    message_text = "<b>Удалить документ 🗑</b>\nВыберите удаляемый файл\n\n"

    from ..database.requests import get_files
    files = await get_files(callback_query.from_user.id)
    counter = 0
    buttons_row = []
    buttons = []
    if len(files) == 0:
        message_text += "У вас ещё нет ни одного документа\n"
    while counter < len(files):
        message_text += f'{counter + 1} - {files[counter].filename}\n'
        buttons_row.append(
            types.InlineKeyboardButton(
                text=str(counter + 1),
                callback_data=f'delete_{files[counter].file_id}'
            )
        )
        if len(buttons_row) == 5:
            buttons.append(buttons_row)
            buttons_row = []
        counter += 1
    if len(buttons_row) != 5:
        buttons.append(buttons_row)
    
    buttons.append(
        [
            assets.inline_keyboards.main_button, 
            assets.inline_keyboards.methods_button
        ]
    )
    message_text += "\n" + assets.message_text.main_menu_vector
    message_text += "\n" + assets.message_text.methods_menu_vector
    message_text += "\n" + assets.message_text.delete_button_vector
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback_query.message.edit_text(
        text=message_text,
        reply_markup=keyboard
    )
    await callback_query.answer()
    

@dp.callback_query(lambda query: query.data.startswith('delete_'))
async def cmd_delete_document(callback_query: types.CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()
    file_id = callback_query.data.split('delete_')[1]
    from ..database.requests import get_file
    file_from_db = await get_file(file_id)
    await callback_query.message.answer(
        text="Ваш файл {} удаляется, пожалуйста, подождите...".format(file_from_db.filename),
    )
    
    # delete from database
    from ..database.requests import delete_file
    await delete_file(file_id, callback_query.from_user.id)
    
    # delete from google drive
    from ..modules.pyDrive import GDrive
    from ..local_settings import credentials, scope
    drive = GDrive(credentials, scope)
    drive.DeleteFile(file_id)
    
    await callback_query.message.answer(
            text=assets.message_text.success_delete_message.format(file_from_db.filename),
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        assets.inline_keyboards.main_button,
                        assets.inline_keyboards.methods_button,
                        assets.inline_keyboards.library_button,
                    ]
                ]
            )
        )
    


@dp.callback_query(DocIDFilter(lambda query: query.data))
async def cmd_document(callback_query: types.CallbackQuery):
    from ..modules.pyDrive import conn_google_drive
    from ..local_settings import credentials, scope
    from ..database.requests import get_file
    from ..database.requests import get_profile
    
    profile = await get_profile(callback_query.from_user.id)
    await callback_query.answer()
    await callback_query.message.delete()
    if profile is None:
        await callback_query.message.answer(
            text=assets.message_text.must_register_message,
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [assets.reply_keyboards.register_button],
                ]
            )
        )
        return
    else:
        file_id = callback_query.data
        file_from_db = await get_file(file_id)
        await callback_query.message.answer(
            text="Ваш файл {} загружается, пожалуйста, подождите...".format(file_from_db.filename),
        )
        drive = await conn_google_drive(credentials, scope)
        file_path = drive.GetFile(title=file_from_db.filename, FileID=file_from_db.file_id, folder_path='temp/files')
        if file_from_db.telegram_id != callback_query.from_user.id:
            new_file = drive.SendFile(file_path=file_path, title=file_from_db.filename, folder_parent=profile.google_folder_id)
            from ..database.requests import add_file
            await add_file(
                file_id=new_file['id'],
                filename=file_from_db.filename,
                parent_folder_id=profile.google_folder_id,
                telegram_id=callback_query.from_user.id
            )
        url = "https://drive.google.com/file/d/{}/view".format(file_from_db.file_id)
        try:
            import telebot
            from ..bot_app import API_TOKEN
            sync_bot = telebot.TeleBot(API_TOKEN)
            sync_bot.send_document(chat_id=callback_query.from_user.id, document=open(file_path, 'rb'))
        except:
            await callback_query.message.answer(
                text=f'<a href="{url}">{file_from_db.filename}</a>',
            )
        
        await callback_query.message.answer(
            text=assets.message_text.success_upload_message,
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        assets.inline_keyboards.new_document_button,
                        assets.inline_keyboards.library_button,
                        assets.inline_keyboards.methods_button,
                        assets.inline_keyboards.main_button
                    ]
                ]
            )
        )
        import os
        os.remove(file_path)
        return
    
    
@dp.callback_query(MyFilter(assets.inline_keyboards.profile_button.callback_data))
async def cmd_profile(callback_query: types.CallbackQuery):
    from ..database.requests import get_profile
    profile = await get_profile(callback_query.from_user.id)
    if profile is None:
        await callback_query.message.answer(
            text=assets.message_text.must_register_message,
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[[assets.reply_keyboards.register_button], [assets.reply_keyboards.menu_button]], 
                resize_keyboard=True)
        )
    else:
        await callback_query.message.answer(
            text=assets.message_text.profile_message.format(
                profile_name=profile.profile_name,
                job_title=profile.job_title,
                bio=profile.bio
            ),
            reply_markup=types.ReplyKeyboardMarkup(
                keyboard=[
                    [assets.reply_keyboards.menu_button],
                    [assets.reply_keyboards.edit_profile_button]
                ],
            )
        )
        await callback_query.answer()
    await callback_query.answer()
