from aiogram import types, Router
from aiogram.filters import Filter

from ..bot_app import dp

router = Router(name=__name__)

class MyFilter(Filter):
    def __init__(self, check_data: str) -> None:
        self.check_data = check_data
        
    async def __call__(self, message: types.Message) -> bool:
        import json
        data = json.loads(message.web_app_data.data)
        return self.check_data == data['action']


@dp.message(MyFilter(check_data="document_request"))
async def document_request(message: types.Message):
    import json
    data = json.loads(message.web_app_data.data)
    flag = await add_request(
        user=message.from_user.id, 
        studnum=data['studnum'], 
        studname=data['studname'], 
        organisation=data['organisation']
    )
    if not flag:
        message_text = \
f'''
<b>Получена новая заяка на:</b>

Имя: {data['studname']}
Студенческий билет: №{data['studnum']}
Для {data['organisation']}

Ожидайте уведомление.
'''
    else:
        message_text = "Заяка уже есть"
    await message.answer(message_text)


@dp.message(MyFilter(check_data="get_graph"))
async def get_graph(message: types.Message):
    import json
    
    from ..database.models import Graph
    
    data: dict = json.loads(message.web_app_data.data)
    studgroup = data["studgroup"]
    week_type = data["week_type"]
    day_of_week = data["day_of_week"]
    week = 'Знаменатель' if week_type == 'Знам.' else 'Числитель'
    result = await get_graph_info(studgroup, day_of_week, week_type)
    message_text = f'<b>Группа:</b> {studgroup}\n<b>Неделя:</b> {week}\n<b>День недели:</b> {day_of_week}\n\n'
    for res in result:
        res: Graph
        if res.studgroup.split('_')[1] == studgroup and res.week_type == week_type and res.day_of_week == day_of_week:
            message_text += (
                f'\n<b>Время:</b> {res.time}\n<b>Дисциплина:</b>\n{res.info.strip()}\n')
    await message.answer(message_text)


@dp.message(MyFilter(check_data="reg_user"))
async def reg_user(message: types.Message):
    import json
    data = json.loads(message.web_app_data.data)
    res = await create_stud(
        user=message.from_user.id,
        studnum=data['studnum'],
        studname=data['studname'],
        studgroup=data['studgroup'],
        studyear=data['studyear']
    )
    if not res:
        message_text = "Регистрация прошла успешно!"
    else: 
        message_text = "Вы уже зарегистрированы!"
    await message.answer(message_text)
        
