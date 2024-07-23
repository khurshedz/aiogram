from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboard():
    button_loan = KeyboardButton('📋 Хочу взять займ')
    button_refinance = KeyboardButton('✂ Хочу рефинансировать займ')
    button_problem = KeyboardButton('✏ Есть проблема или вопрос')
    button_contact = KeyboardButton('📞 Поделиться номером', request_contact=True)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(button_loan, button_refinance, button_problem,
                                                             button_contact)
    return keyboard


async def get_loan_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Онлайн'))
    keyboard.add(KeyboardButton('Офлайн'))
    return keyboard


async def get_online_application_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Оформить заявку'))
    keyboard.add(KeyboardButton('Назад'))
    return keyboard


async def get_offline_application_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Оформить заявку'))
    keyboard.add(KeyboardButton('Назад'))
    return keyboard


async def get_problem_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Связаться с поддержкой'))
    keyboard.add(KeyboardButton('Назад'))
    return keyboard


async def get_refinance_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Рефинансировать кредит'))
    keyboard.add(KeyboardButton('Рефинансировать ипотеку'))
    keyboard.add(KeyboardButton('Назад'))
    return keyboard
