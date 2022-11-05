from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --------------------------------- Back to Menu ---------------------------------
button_menu = KeyboardButton('🔙 Вернуться в главное меню')
# ---------------------------------------------------------------------------------------------------

# --------------------------------- Main Menu ---------------------------------
# button_terms = KeyboardButton('🤝 Условия сотрудничества')
button_price = KeyboardButton('🧾 Рассчитать стоимость')
button_support = KeyboardButton('🆘 Поддержка / Жалобы')
button_promo = KeyboardButton('🎁 Скидки / Промокоды')
button_ref = KeyboardButton('📢 Реферальная система')
button_about = KeyboardButton('ℹ О нас')
mainMenu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_about).add(button_price).row(
    button_promo, button_ref).add(button_support)
# ---------------------------------------------------------------------------------------------------

# --------------------------------- Price Menu ---------------------------------
button_tailoring = KeyboardButton('🪡🧵 Индивидуальный пошив')
button_done = KeyboardButton('👕 Готовая продукция')
button_cloth = KeyboardButton('🧶 Ткани')
priceMenu_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_tailoring).row(button_cloth,
                                                                                                           button_done) \
    .add(button_menu)
# ---------------------------------------------------------------------------------------------------

# --------------------------------- Registration Menu ---------------------------------
markup_request = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
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

# --------------------------------- Social Networks ---------------------------------
button_tg = KeyboardButton('Telegram')
button_wa = KeyboardButton('WhatsApp')
button_vk = KeyboardButton('ВКонтакте')
social_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_tg).add(button_wa).add(
    button_vk)
# ----------------------------------------------------------------------------------------------------

# --------------------------------- Skip ---------------------------------
button_skip = KeyboardButton('Пропустить')
skip_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_skip)
# ----------------------------------------------------------------------------------------------------

# --------------------------------- Stop ---------------------------------
button_stop = KeyboardButton('🛑 Прекратить отправку фото')
stop_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_stop)
# ----------------------------------------------------------------------------------------------------
