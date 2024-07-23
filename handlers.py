import time
from aiogram import types
import logging

class Handlers:
    def __init__(self, dp, db_manager, keyboards, request_interval=1):
        self.dp = dp
        self.db_manager = db_manager
        self.keyboards = keyboards
        self.REQUEST_INTERVAL = request_interval
        self.user_last_request_time = {}

        # Регистрация обработчиков
        self.dp.register_message_handler(self.send_welcome, commands=['start', 'help'])
        self.dp.register_message_handler(self.handle_loan, lambda message: message.text == "📋 Хочу взять займ")
        self.dp.register_message_handler(self.handle_refinance, lambda message: message.text == "✂ Хочу рефинансировать займ")
        self.dp.register_message_handler(self.handle_problem, lambda message: message.text == "✏ Есть проблема или вопрос")
        self.dp.register_message_handler(self.handle_contact, content_types=types.ContentType.CONTACT)

    async def check_request_interval(self, message: types.Message):
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

    async def send_welcome(self, message: types.Message):
        if not await self.check_request_interval(message):
            return

        welcome_text = (
            "Я — бот Деньга. Помогу:\n"
            "1️⃣ Выбрать и оформить займ\n"
            "2️⃣ Рефинансировать старый займ\n"
            "3️⃣ Связаться с нужным специалистом\n"
            "📞 Поделиться номером телефона"
        )
        await message.reply(welcome_text, reply_markup=self.keyboards.get_main_keyboard())

    async def handle_loan(self, message: types.Message):
        if not await self.check_request_interval(message):
            return

        await message.reply("Вы выбрали: Хочу взять займ")

    async def handle_refinance(self, message: types.Message):
        if not await self.check_request_interval(message):
            return

        await message.reply("Вы выбрали: Хочу рефинансировать займ")

    async def handle_problem(self, message: types.Message):
        if not await self.check_request_interval(message):
            return

        await message.reply("Вы выбрали: Есть проблема или вопрос")

    async def handle_contact(self, message: types.Message):
        if not await self.check_request_interval(message):
            return

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
