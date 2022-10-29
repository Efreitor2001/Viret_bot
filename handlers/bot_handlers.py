from aiogram import types
from aiogram.dispatcher import FSMContext
from create_bot import bot, dp
from fsms import *
from buttons import *
import psycopg2
from psycopg2 import OperationalError, Error


def create_connection():
    connection = None
    try:
        connection = psycopg2.connect(database="Viret",  # Название БД
                                      user="Efreitor2001",  # Логин
                                      password="Antelope1",  # Пароль
                                      host="127.0.0.1",  # Хост
                                      port="5432"  # Порт
                                      )
        print("Успешное подключение к БД")
    except OperationalError as e:
        print(f"Ошибка при подключении к БД: '{e}'")
    return connection


def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
    print("Соединение с БД успешно закрыто")


async def hi(message):
    if message.text == '📧 Отправить е-майл':
        await bot.send_message(message.chat.id, "Ждём Ваш е-майл 😉\n(Нужно отправить вручную)")
    elif "@" in message.text or "mail" in message.text:
        get_user_email(message)
        await bot.send_message(message.chat.id, "Почта получена, приступаем)", reply_markup=mainMenu_kb)
    if message.text == '🤝 Условия сотрудничества':
        await bot.send_message(message.chat.id, 'Тут бот скинет условия', reply_markup=mainMenu_kb)
    elif message.text == '🪡🧵 Пошив':
        await bot.send_message(message.chat.id, 'Тут бот скинет инфу по пошиву', reply_markup=mainMenu_kb)
    elif message.text == '☑ Готовая продукция':
        await bot.send_message(message.chat.id, 'Тут бот скинет инфу по готовой продукции', reply_markup=mainMenu_kb)
    elif message.text == 'ℹ О нас':
        await bot.send_message(message.chat.id, 'Тут бот скинет инфу о компании', reply_markup=mainMenu_kb)
    elif message.text == '🧶 Ткани':
        await bot.send_message(message.chat.id, 'Как Вас зовут?')
        await ClothStates.name.set()
    elif message.text == '!клава':
        await bot.send_message(message.chat.id, 'клава', reply_markup=mainMenu_kb)


async def start(message):
    await bot.send_message(message.chat.id, "Для продолжения работы необходимо поделиться контактом...",
                           reply_markup=markup_request)


async def get_user_information(message):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        user = [(message.from_user.first_name, message.from_user.last_name, message.contact.phone_number,
                 message.from_user.id)]
        user_records = ", ".join(["%s"] * len(user))
        insert_query = (
            f"INSERT INTO users (name, surname, phone, tg_user_id) VALUES {user_records}"
        )
        connection.autocommit = True
        cursor.execute(insert_query, user)
    except (Exception, Error) as error:
        print(f"Ошибка при работе с БД: {error}")
    finally:
        close_connection(connection, cursor)
        await bot.send_message(message.chat.id, 'Последний шаг! Отправьте нам Ваш адрес электронной почты для связи...',
                               reply_markup=email_kb)


def get_user_email(message):
    connection = create_connection()
    cursor = connection.cursor()
    try:
        user_email = message.text
        insert_query = (
            f"UPDATE users SET email = '{message.text}', email_check = TRUE WHERE tg_user_id = {message.from_user.id} "
            f"AND email_check IS FALSE"
        )
        connection.autocommit = True
        cursor.execute(insert_query, user_email)
    except (Exception, Error) as error:
        print(f"Ошибка при работе с БД: {error}")
    finally:
        close_connection(connection, cursor)


# async def photo_checker(message: types.Message):
#     if message.text != 'Пропустить':
#         await message.reply('Это не фотография!')
#     else:
#         await bot.send_message(message.chat.id, 'Напишите нужный метраж на артикул/цвет')
#         await ClothStates.footage.set()


async def get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(message.chat.id, "Из какого Вы города?")
    await ClothStates.next()


async def get_city(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['city'] = message.text
    await bot.send_message(message.chat.id, "Пришлите название нужных Вам тканей (через запятую)")
    await ClothStates.next()


async def get_clothes_names(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['clothes_names'] = message.text
    await bot.send_message(message.chat.id, "Отправьте примерное фото расцветок (Можно пропустить)",
                           reply_markup=skip_kb)
    await ClothStates.next()


async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text != 'Пропустить':
            data['photo'] = message.photo[0].file_id
        else:
            data['photo'] = message.text
    await bot.send_message(message.chat.id, "Напишите нужный метраж на артикул/цвет")
    await ClothStates.next()


async def get_footage(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['footage'] = message.text
    await bot.send_message(message.chat.id, "Нужно ли Вам отправлять кусочки тканей?\n(СДЕКом (800-1400р))",
                           reply_markup=yesOrNo_kb)
    await ClothStates.next()


async def get_samples(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['samples'] = message.text
    await bot.send_message(message.chat.id, "Нужна ли Вам услуга проверки на текстиьный брак и недостаток метража?",
                           reply_markup=yesOrNo_kb)
    await ClothStates.next()


async def get_check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['check'] = message.text
    await bot.send_message(message.chat.id, "Ваш способ оплаты?", reply_markup=payment_kb)
    await ClothStates.next()


async def get_payment_method(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['payment_method'] = message.text
        print(data)
    await bot.send_message(message.chat.id, "Завка запонена!", reply_markup=mainMenu_kb)
    await state.finish()


def register_handlers_bot_handlers(dp: dp):
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(get_user_information, content_types='contact')
    dp.register_message_handler(hi)
    # dp.register_message_handler(photo_checker, lambda message: not message.photo, state=ClothStates.photo)
    dp.register_message_handler(get_name, state=ClothStates.name)
    dp.register_message_handler(get_city, state=ClothStates.city)
    dp.register_message_handler(get_clothes_names, state=ClothStates.clothes_names)
    dp.register_message_handler(get_photo, state=ClothStates.photo)
    dp.register_message_handler(get_footage, state=ClothStates.footage)
    dp.register_message_handler(get_samples, state=ClothStates.samples)
    dp.register_message_handler(get_check, state=ClothStates.check)
    dp.register_message_handler(get_payment_method, state=ClothStates.payment_method)
