from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
import re

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


async def main(message):
    if message.text == '📧 Отправить е-майл':
        await bot.send_message(message.chat.id, "Ждём Ваш е-майл 😉\n(Нужно отправить вручную)")
    elif "@" in message.text or "mail" in message.text:
        get_user_email(message)
        await bot.send_message(message.chat.id, "Почта получена, приступаем)", reply_markup=mainMenu_kb)
    if message.text == '🤝 Условия сотрудничества':
        await bot.send_message(message.chat.id, 'Тут бот скинет условия', reply_markup=mainMenu_kb)
    elif message.text == '🪡🧵 Индивидуальный пошив':
        await bot.send_message(message.chat.id, 'Как Вас зовут?')
        await TailoringStates.name.set()
    elif message.text == '👕 Готовая продукция':
        await bot.send_message(message.chat.id, 'Тут бот скинет инфу по готовой продукции', reply_markup=mainMenu_kb)
    elif message.text == 'ℹ О нас':
        await bot.send_message(message.chat.id, 'Тут бот скинет инфу о компании', reply_markup=mainMenu_kb)
    elif message.text == '🧶 Ткани':
        await bot.send_message(message.chat.id, 'Как Вас зовут?')
        await ClothStates.name.set()
    elif message.text == '🧾 Рассчитать стоимость':
        await bot.send_message(message.chat.id, 'Рассчитать стоимость', reply_markup=priceMenu_kb)
    elif message.text == '🔙 Вернуться в главное меню':
        await bot.send_message(message.chat.id, 'Выход в главное меню', reply_markup=mainMenu_kb)
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
        await bot.send_message(message.chat.id, 'Последний шаг! Отправьте нам Ваш адрес электронной почты для связи...')
        await EmailStates.email.set()


async def get_user_email(message, state: FSMContext):
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
        await bot.send_message(message.chat.id, 'Почта успешно получена!', reply_markup=mainMenu_kb)
        await state.finish()


# --------------------------------- Clothes States ---------------------------------
async def photo_checker_clothes(message: types.Message):
    if message.text != 'Пропустить':
        await message.reply('Это не фотография!')
    else:
        await bot.send_message(message.chat.id, 'Напишите нужный метраж на артикул/цвет')
        await ClothStates.footage.set()


async def get_name_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await bot.send_message(message.chat.id, "Пришлите название нужных Вам тканей (через запятую)")
    await ClothStates.next()


# async def get_city(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['city'] = message.text
#     await bot.send_message(message.chat.id, "Пришлите название нужных Вам тканей (через запятую)")
#     await ClothStates.next()


async def get_clothes_names_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['clothes_names'] = message.text
    await bot.send_message(message.chat.id, "Отправьте примерное фото расцветок (Можно пропустить)",
                           reply_markup=skip_kb)
    await ClothStates.next()


async def get_photo_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await bot.send_message(message.chat.id, "Напишите нужный метраж на артикул/цвет")
    await ClothStates.next()


async def get_footage_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['footage'] = message.text
    await bot.send_message(message.chat.id, "Нужно ли Вам отправлять кусочки тканей?\n(СДЕКом (800-1400р))",
                           reply_markup=yesOrNo_kb)
    await ClothStates.next()


async def get_samples_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['samples'] = message.text
    await bot.send_message(message.chat.id, "Нужна ли Вам услуга проверки на текстиьный брак и недостаток метража?",
                           reply_markup=yesOrNo_kb)
    await ClothStates.next()


async def get_check_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['check'] = message.text
    await bot.send_message(message.chat.id, "Ваш способ оплаты?", reply_markup=payment_kb)
    await ClothStates.next()


async def get_payment_method_clothes(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['payment_method'] = message.text
        print(data)
    if 'photo' in data:
        await bot.send_photo(message.chat.id,
                             photo=data['photo'],
                             caption=f"Имя: {data['name']}\n"
                                     f"Ткани: {data['clothes_names']}\n"
                                     f"Метраж: {data['footage']}\n"
                                     f"Образцы тканей: {data['samples']}\n"
                                     f"Проверка на брак / метраж: {data['check']}\n"
                                     f"Способ оплаты: {data['payment_method']}")
    else:
        no_photo = InputFile("photos/no_photo.jpg")
        await bot.send_photo(message.chat.id,
                             photo=no_photo,
                             caption=f"Имя: {data['name']}\n"
                                     f"Ткани: {data['clothes_names']}\n"
                                     f"Метраж: {data['footage']}\n"
                                     f"Образцы тканей: {data['samples']}\n"
                                     f"Проверка на брак / метраж: {data['check']}\n"
                                     f"Способ оплаты: {data['payment_method']}")
    await bot.send_message(message.chat.id, "Завка запонена!", reply_markup=mainMenu_kb)
    await state.finish()


# ---------------------------------------------------------------------------------------------------

# --------------------------------- Tailoring States ---------------------------------
async def get_name_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['name_tailoring'] = message.text
    await bot.send_message(message.chat.id, "Пришлите фото моделей, которые хотетите отшить")
    await TailoringStates.next()


async def get_photo_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['photo_tailoring'] = message.photo[0].file_id
    await bot.send_message(message.chat.id, "Какое количество Вы хотите отшить?")
    await TailoringStates.next()


async def get_count_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['count_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Есть готовые лекала или образец на эту модель?',
                           reply_markup=yesOrNo_kb)
    await TailoringStates.next()


async def sample_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['sample_tailoring'] = message.text
    if message.text == 'Да':
        await bot.send_message(message.chat.id, 'Пришлите фото лекала или образца')
        await TailoringStates.next()
    else:
        await bot.send_message(message.chat.id, 'Знаете ли Вы название подходящих тканей?', reply_markup=yesOrNo_kb)
        await TailoringStates.cloth_names_quest.set()


async def sample_photo_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['sample_photo_tailoring'] = message.photo[0].file_id
    await bot.send_message(message.chat.id, 'Знаете ли Вы название подходящих тканей?', reply_markup=yesOrNo_kb)
    await TailoringStates.next()


async def cloth_names_quest_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['cloth_names_quest_tailoring'] = message.text
    if message.text == 'Да':
        await bot.send_message(message.chat.id, 'Пришлите название тканей (через запятую)')
        await TailoringStates.next()
    else:
        await bot.send_message(message.chat.id, 'Изделия будут под Вашим брендом?', reply_markup=yesOrNo_kb)
        await TailoringStates.brand.set()


async def cloth_names_list_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['cloth_names_list_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Изделия будут под Вашим брендом?', reply_markup=yesOrNo_kb)
    await TailoringStates.next()


async def brand_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['brand_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Нужна ли Вам маркировка?', reply_markup=yesOrNo_kb)
    await TailoringStates.next()


async def mark_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['mark_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Нужно ли Вам сделать декларацию соответсвия?', reply_markup=yesOrNo_kb)
    await TailoringStates.next()


async def declaration_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['declaration_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Фотосессию сделать Нам?', reply_markup=yesOrNo_kb)
    await TailoringStates.next()


async def photoshoot_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['photoshoot_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Укажите способ оплаты', reply_markup=payment_kb)
    await TailoringStates.next()


async def get_payment_method_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['payment_method_tailoring'] = message.text
        print(data_tailoring)
    await bot.send_message(message.chat.id, "Где Вам было бы удобнее продолжить общение с менеджером?",
                           reply_markup=social_kb)
    await TailoringStates.next()


async def manager_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['manager_tailoring'] = message.text
    await bot.send_message(message.chat.id, 'Укажите Ваш телефон / ссылку которые привязаны к указанному мессенджеру')
    await TailoringStates.next()


async def phone_tailoring(message: types.Message, state: FSMContext):
    async with state.proxy() as data_tailoring:
        data_tailoring['phone_tailoring'] = message.text
    await bot.send_message(message.chat.id, "Завка запонена!", reply_markup=mainMenu_kb)
    await state.finish()


# ---------------------------------------------------------------------------------------------------
def register_handlers_bot_handlers(dp: dp):
    # --------------------------------- Registration Handlers ---------------------------------
    dp.register_message_handler(start, commands='start')
    dp.register_message_handler(get_user_information, content_types='contact')
    dp.register_message_handler(get_user_email, state=EmailStates.email)
    # ---------------------------------------------------------------------------------------------------

    # --------------------------------- Main Handler ---------------------------------
    dp.register_message_handler(main)
    # ---------------------------------------------------------------------------------------------------

    # --------------------------------- Clothes Handlers ---------------------------------
    dp.register_message_handler(photo_checker_clothes, lambda message: not message.photo, state=ClothStates.photo)
    dp.register_message_handler(get_name_clothes, state=ClothStates.name)
    # dp.register_message_handler(get_city, state=ClothStates.city)
    dp.register_message_handler(get_clothes_names_clothes, state=ClothStates.clothes_names)
    dp.register_message_handler(get_photo_clothes, content_types='photo', state=ClothStates.photo)
    dp.register_message_handler(get_footage_clothes, state=ClothStates.footage)
    dp.register_message_handler(get_samples_clothes, state=ClothStates.samples)
    dp.register_message_handler(get_check_clothes, state=ClothStates.check)
    dp.register_message_handler(get_payment_method_clothes, state=ClothStates.payment_method)
    # ---------------------------------------------------------------------------------------------------

    # --------------------------------- Tailoring Handlers ---------------------------------
    dp.register_message_handler(get_name_tailoring, state=TailoringStates.name)
    dp.register_message_handler(get_photo_tailoring, content_types='photo', state=TailoringStates.photo)
    dp.register_message_handler(get_count_tailoring, state=TailoringStates.count)
    dp.register_message_handler(sample_tailoring, state=TailoringStates.sample)
    dp.register_message_handler(sample_photo_tailoring, state=TailoringStates.sample_photo)
    dp.register_message_handler(cloth_names_quest_tailoring, state=TailoringStates.cloth_names_quest)
    dp.register_message_handler(cloth_names_list_tailoring, state=TailoringStates.cloth_names_list)
    dp.register_message_handler(brand_tailoring, state=TailoringStates.brand)
    dp.register_message_handler(mark_tailoring, state=TailoringStates.mark)
    dp.register_message_handler(declaration_tailoring, state=TailoringStates.declaration)
    dp.register_message_handler(photoshoot_tailoring, state=TailoringStates.photoshoot)
    dp.register_message_handler(get_payment_method_tailoring, state=TailoringStates.payment_method)
    dp.register_message_handler(manager_tailoring, state=TailoringStates.manager)
    dp.register_message_handler(phone_tailoring, state=TailoringStates.phone)
    # ---------------------------------------------------------------------------------------------------
