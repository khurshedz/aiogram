import time
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message, ContentType
import logging
import functools


class Form(StatesGroup):
    loan_choice = State()
    refinance_choice = State()
    problem_choice = State()
    online_application = State()
    offline_application = State()
    personal_loan = State()
    mortgage = State()
    consumer_loan = State()
    date_choice = State()
    success = State()
    contact = State()


def check_interval(func):
    @functools.wraps(func)
    async def wrapper(self, message, *args, **kwargs):
                return await func(self, message, *args, **kwargs)

    return wrapper


class Handlers:
    def __init__(self, dp, db_manager, keyboards, request_interval=1):
        self.dp = dp
        self.db_manager = db_manager
        self.keyboards = keyboards
        self.REQUEST_INTERVAL = request_interval
        self.user_last_request_time = {}

        # Регистрация обработчиков
        self.dp.register_message_handler(self.send_welcome, commands=['start', 'help'])
        self.dp.register_message_handler(self.handle_loan, lambda message: message.text == "📋 Хочу взять займ",
                                         state='*')
        self.dp.register_message_handler(self.handle_refinance,
                                         lambda message: message.text == "✂ Хочу рефинансировать займ", state='*')
        self.dp.register_message_handler(self.handle_problem,
                                         lambda message: message.text == "✏ Есть проблема или вопрос", state='*')
        self.dp.register_message_handler(self.handle_contact, content_types=ContentType.CONTACT, state='*')

        # Регистрация FSM обработчиков
        self.dp.register_message_handler(self.loan_choice, state=Form.loan_choice)
        # self.dp.register_message_handler(self.refinance_choice, state=Form.refinance_choice)
        # self.dp.register_message_handler(self.problem_choice, state=Form.problem_choice)
        # self.dp.register_message_handler(self.online_application, state=Form.online_application)
        # self.dp.register_message_handler(self.offline_application, state=Form.offline_application)
        # self.dp.register_message_handler(self.personal_loan, state=Form.personal_loan)
        # self.dp.register_message_handler(self.mortgage, state=Form.mortgage)
        # self.dp.register_message_handler(self.consumer_loan, state=Form.consumer_loan)
        # self.dp.register_message_handler(self.date_choice, state=Form.date_choice)
        # self.dp.register_message_handler(self.success, state=Form.success)

    async def check_request_interval(self, message: Message):
        user_id = message.from_user.id
        current_time = time.time()

        # Проверка времени последнего запроса
        if user_id in self.user_last_request_time:
            last_request_time = self.user_last_request_time[user_id]
            if current_time - last_request_time < self.REQUEST_INTERVAL:
                await message.reply("Вы слишком часто нажимаете кнопку.")
                return False

        # Обновление времени последнего запроса
        self.user_last_request_time[user_id] = current_time
        return True

    @check_interval
    async def send_welcome(self, message: Message):
        
        welcome_text = (
            "Я — бот Деньга. Помогу:\n"
            "1️⃣ Выбрать и оформить займ\n"
            "2️⃣ Рефинансировать старый займ\n"
            "3️⃣ Связаться с нужным специалистом\n"
        )
        await message.reply(welcome_text, reply_markup=self.keyboards.get_main_keyboard())

    @check_interval
    async def handle_loan(self, message: Message):
        await Form.loan_choice.set()
        await message.reply("Какой вид займа вас интересует?", reply_markup=self.get_loan_keyboard())

    @check_interval
    async def handle_refinance(self, message: Message):
        await Form.refinance_choice.set()
        await message.reply("Вы выбрали: Хочу рефинансировать займ",) # reply_markup=self.get_refinance_keyboard())

    @check_interval
    async def handle_problem(self, message: Message):
        await Form.problem_choice.set()
        await message.reply("Вы выбрали: Есть проблема или вопрос")

    @check_interval
    async def handle_contact(self, message: Message):
        
        contact = message.contact
        phone_number = contact.phone_number
        user_id = contact.user_id
        first_name = contact.first_name
        last_name = contact.last_name

        # Логируем номер телефона и пользователя
        logging.info(
            f"User ID: {user_id}, First Name: {first_name}, Last Name: {last_name}, Phone Number: {phone_number}")

        # Сохраняем контакт в базу данных
        await self.db_manager.save_contact(user_id, first_name, last_name, phone_number)

        await message.reply("Спасибо за предоставленный номер телефона!")

    @check_interval
    async def loan_choice(self, message: Message, state: FSMContext):
        if message.text == 'Онлайн':
            await Form.online_application.set()
            await message.reply("Вы выбрали онлайн-заявку. Что бы вы хотели сделать?",
                                reply_markup=self.get_online_application_keyboard())
        elif message.text == 'Офлайн':
            await Form.offline_application.set()
            await message.reply("Вы выбрали офлайн-заявку. Что бы вы хотели сделать?",
                                reply_markup=self.get_offline_application_keyboard())
        else:
            await message.reply("Пожалуйста, выберите один из предложенных вариантов.")

    @check_interval
    async def get_loan_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Онлайн'))
        keyboard.add(KeyboardButton('Офлайн'))
        return keyboard

    @check_interval
    async def get_online_application_keyboard(self):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Оформить заявку'))
        keyboard.add(KeyboardButton('Назад'))
        return keyboard

    @check_interval
    async def get_offline_application_keyboard(self, message: Message):
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(KeyboardButton('Выбрать город'))
        await message.reply("Вы выбрали: Оффлайн")