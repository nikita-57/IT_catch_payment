from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging

# Укажи свой токен напрямую
TOKEN = "6782021076:AAGy-0Hn-PWIpviHnOHx_slOllQSA9-E3Yw"
ADMIN_ID = "620210761"  # Укажи ID администратора (например, свой Telegram ID)

# Создание объекта бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Включение логирования для отладки
logging.basicConfig(level=logging.INFO)

# Создание кнопок для выбора курса
inline_kb_courses = InlineKeyboardMarkup(row_width=1)  # Кнопки будут расположены в один столбец
button1 = InlineKeyboardButton('Курс 1: Python для начинающих', callback_data='course1')
button2 = InlineKeyboardButton('Курс 2: Продвинутый Python', callback_data='course2')
button3 = InlineKeyboardButton('Курс 3: Веб-разработка на Django', callback_data='course3')
button4 = InlineKeyboardButton('Курс 4: Сетевой инженер', callback_data='course4')
inline_kb_courses.add(button1, button2, button3, button4)

# Кнопки для дополнительной логики
def get_course_options_markup(course_id):
    markup = InlineKeyboardMarkup(row_width=2)
    button_details = InlineKeyboardButton('Подробнее', callback_data=f'details_{course_id}')
    button_enroll = InlineKeyboardButton('Записаться', callback_data=f'enroll_{course_id}')
    markup.add(button_details, button_enroll)
    return markup

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # Приветственное сообщение
    welcome_text = (
        "Привет, {0.first_name}!\n"
        "Добро пожаловать в наш учебный бот.\n"
        "Мы предлагаем курсы на любой вкус! Пожалуйста, выбери интересующий тебя курс из списка ниже."
    ).format(message.from_user)
    
    # Отправляем приветственное сообщение
    await message.reply(welcome_text)
    
    # Предлагаем выбрать курс
    await message.answer("Выбери подходящий курс:", reply_markup=inline_kb_courses)

# Обработчик нажатий на кнопки курсов
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('course'))
async def process_course_selection(callback_query: types.CallbackQuery):
    course_id = callback_query.data
    course_name = ""
    if course_id == 'course1':
        course_name = 'Python для начинающих'
    elif course_id == 'course2':
        course_name = 'Продвинутый Python'
    elif course_id == 'course3':
        course_name = 'Веб-разработка на Django'
    elif course_id == 'course4':
        course_name = 'Сетевой инженер'  # Исправлено присвоение значения

    await bot.send_message(callback_query.from_user.id, f'Ты выбрал курс: {course_name}')

    # Показать описание и предложить дополнительные опции
    await bot.send_message(callback_query.from_user.id, 
                           f'Описание курса "{course_name}":\nЭто отличный курс для тех, кто хочет научиться {course_name.lower()} с нуля.',
                           reply_markup=get_course_options_markup(course_id))

    await bot.answer_callback_query(callback_query.id)

# Обработчик нажатий на дополнительные опции
@dp.callback_query_handler(lambda c: c.data and c.data.startswith(('details_', 'enroll_')))
async def process_additional_options(callback_query: types.CallbackQuery):
    action, course_id = callback_query.data.split('_')
    
    if action == 'details':
        # Показываем подробную информацию о курсе
        await bot.send_message(callback_query.from_user.id, f'Подробная программа курса {course_id}: ...\n(здесь может быть детальное описание программы)')
    elif action == 'enroll':
        # Отправляем сообщение админу
        user_info = callback_query.from_user
        course_name = ""
        if course_id == 'course1':
            course_name = 'Python для начинающих'
        elif course_id == 'course2':
            course_name = 'Продвинутый Python'
        elif course_id == 'course3':
            course_name = 'Веб-разработка на Django'
        elif course_id == 'course4':
            course_name = 'Сетевой инженер'  # Исправлено присвоение значения

        admin_message = (
            f"Пользователь {user_info.full_name} (@{user_info.username}) хочет записаться на курс: {course_name}.\n"
            f"ID пользователя: {user_info.id}"
        )
        await bot.send_message(ADMIN_ID, admin_message)

        # Подтверждаем пользователю
        await bot.send_message(callback_query.from_user.id, f'Вы успешно записались на курс {course_name}!\nНаш менеджер свяжется с вами в ближайшее время.')

    await bot.answer_callback_query(callback_query.id)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)