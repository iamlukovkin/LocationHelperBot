# repeatable text
main_menu_vector = "📍 - Главное меню"
methods_menu_vector = "📚 - Методические указания"
profile_menu_vector = "👤 - Профиль"

start_message = "Привет! Ты находишься на главной странице бота Локация.Помощник📍 \nЭтот бот поможет тебе упростить работу в смене. Давай скорее же начнем!🤓"
menu_message = "<b>Главное меню</b>:\n\n📚 - Методические указания\n📖 - Педагогический дневник\nℹ️ -Помощь по навигации\n👤 - Профиль"
methods_message = "<b>Методические указания</b>:\n\n🔍 - Найти новый документ\n📔 - Посмотреть личную библиотеку\n📄 - Загрузить новый документ\n" + main_menu_vector
new_document_message = "<b>Найти новый документ🔍</b>\n\n"
success_upload_message = '<b>Документ успешно отправлен</b>\n\nВыберите дальнейшее действие:\n🔍 - Вернуться к поиску\n📚 - Методические указания\n' + main_menu_vector
must_register_message = '<b>❗️Вы не зарегистрированы</b>\n\n📝Для использования всех функций бота необходимо зарегистрироваться'
success_registration_message = '<b>📝Регистрация прошла успешно!</b>\n\n' + main_menu_vector + "\n" + profile_menu_vector
success_edit_profile_message = '<b>📝Профиль изменен</b>\n\n' + main_menu_vector + "\n" + profile_menu_vector
profile_message = '''
<b>👤Профиль</b>

ФИО:
{profile_name}
Должность:
{job_title}
Краткое описание:
{bio}
'''