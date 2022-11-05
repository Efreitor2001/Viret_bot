from aiogram.dispatcher.filters.state import StatesGroup, State


class ClothStates(StatesGroup):  # Машина состояний для Тканей
    name = State()
    # city = State()
    clothes_names = State()
    photo = State()
    footage = State()
    samples = State()
    check = State()
    payment_method = State()


class TailoringStates(StatesGroup):  # Машина состояний для Пошива
    name = State()
    # city = State()
    photo = State()
    count = State()
    sample = State()
    sample_photo = State()
    cloth_names_quest = State()
    cloth_names_list = State()
    brand = State()
    mark = State()
    declaration = State()
    photoshoot = State()
    payment_method = State()
    manager = State()
    phone = State()


class EmailStates(StatesGroup):  # Машина состояний для получения почты юзера
    email = State()
