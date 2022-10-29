from aiogram.dispatcher.filters.state import StatesGroup, State


class ClothStates(StatesGroup):
    name = State()
    city = State()
    clothes_names = State()
    photo = State()
    footage = State()
    samples = State()
    check = State()
    payment_method = State()
