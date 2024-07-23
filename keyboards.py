from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
class Keyboards:
    def __init__(self):
        self.inline_kb = InlineKeyboardMarkup(row_width=4)
        self.button_loan = KeyboardButton('📋 Хочу взять займ')
        self.button_refinance = KeyboardButton('✂ Хочу рефинансировать займ')
        self.button_problem = KeyboardButton('✏ Есть проблема или вопрос')
        self.button_contact = KeyboardButton('📞 Поделиться номером', request_contact=True)
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(self.button_loan, self.button_refinance,
                                                                      self.button_problem, self.button_contact)

    def get_main_keyboard(self):
        return self.keyboard
