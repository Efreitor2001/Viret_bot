from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_mainMenu = KeyboardButton('📲 Главное меню')

# --------------------------------- Main Menu ---------------------------------
# button_terms = KeyboardButton('🤝 Условия сотрудничества')
button_sewing = KeyboardButton('🪡🧵 Пошив')
button_done = KeyboardButton('☑ Готовая продукция')
button_cloth = KeyboardButton('🧶 Ткани')
button_support = KeyboardButton('🆘 Поддержка / Жалобы')
button_promo = KeyboardButton('🎁 Скидки / Промокоды')
button_ref = KeyboardButton('💌 Реферальная система')
button_about = KeyboardButton('ℹ О нас')
mainMenu_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_about).row(button_sewing,
                                                                              button_cloth).add(
    button_done) \
    .row(button_promo, button_ref).add(button_support)
# ---------------------------------------------------------------------------------------------------

# --------------------------------- Registration Menu ---------------------------------
button_email = KeyboardButton('📧 Отправить е-майл')
email_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_email)
markup_request = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)
# ---------------------------------------------------------------------------------------------------

# --------------------------------- Yes or No ---------------------------------
button_yes = KeyboardButton('Да')
button_no = KeyboardButton('Нет')
yesOrNo_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(button_yes, button_no)
# ----------------------------------------------------------------------------------------------------

# --------------------------------- Payment Method ---------------------------------
button_cash = KeyboardButton('Наличными')
button_card = KeyboardButton('Картой')
button_rs = KeyboardButton('Расчётный счёт (+10% к стоимости)')
payment_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_cash, button_card).add(button_rs)
# ----------------------------------------------------------------------------------------------------

# --------------------------------- Skip ---------------------------------
button_skip = KeyboardButton('Пропустить')
skip_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_skip)
# ----------------------------------------------------------------------------------------------------
