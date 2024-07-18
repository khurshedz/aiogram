import logging
import asyncio
import asyncpg
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import config  # Импортируем файл конфигурации


class BotHandler:
    def __init__(self):
        self.bot = Bot(token=config.API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.dp.middleware.setup(LoggingMiddleware())

        # Создание кнопок
        self.button_loan = KeyboardButton('📋 Хочу взять займ')
        self.button_refinance = KeyboardButton('✂ Хочу рефинансировать займ')
        self.button_problem = KeyboardButton('✏ Есть проблема или вопрос')
        self.button_contact = KeyboardButton('📞 Поделиться номером', request_contact=True)
        self.keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(self.button_loan, self.button_refinance,
                                                                      self.button_problem, self.button_contact)

        # Регистрация обработчиков
        self.dp.register_message_handler(self.send_welcome, commands=['start', 'help'])
        self.dp.register_message_handler(self.handle_loan, lambda message: message.text == "📋 Хочу взять займ")
        self.dp.register_message_handler(self.handle_refinance,
                                         lambda message: message.text == "✂ Хочу рефинансировать займ")
        self.dp.register_message_handler(self.handle_problem,
                                         lambda message: message.text == "✏ Есть проблема или вопрос")
        self.dp.register_message_handler(self.handle_contact, content_types=types.ContentType.CONTACT)

        # Инициализация подключения к базе данных
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.init_db())

    async def init_db(self):
        self.pool = await asyncpg.create_pool(
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            database=config.POSTGRES_DB,
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT
        )

    async def send_welcome(self, message: types.Message):
        welcome_text = (
            "Я — бот Деньга. Помогу:\n"
            "1️⃣ Выбрать и оформить займ\n"
            "2️⃣ Рефинансировать старый займ\n"
            "3️⃣ Связаться с нужным специалистом\n"
            "📞 Поделиться номером телефона"
        )
        await message.reply(welcome_text, reply_markup=self.keyboard)

    async def handle_loan(self, message: types.Message):
        await message.reply("Вы выбрали: Хочу взять займ")

    async def handle_refinance(self, message: types.Message):
        await message.reply("Вы выбрали: Хочу рефинансировать займ")

    async def handle_problem(self, message: types.Message):
        await message.reply("Вы выбрали: Есть проблема или вопрос")

    async def handle_contact(self, message: types.Message):
        contact = message.contact
        phone_number = contact.phone_number
        user_id = contact.user_id
        first_name = contact.first_name
        last_name = contact.last_name

        # Логируем номер телефона и пользователя
        logging.info(
            f"User ID: {user_id}, First Name: {first_name}, Last Name: {last_name}, Phone Number: {phone_number}")

        # Сохраняем контакт в базу данных
        async with self.pool.acquire() as connection:
            await connection.execute('''
                INSERT INTO contacts (user_id, first_name, last_name, phone_number) VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_id) DO UPDATE SET phone_number = EXCLUDED.phone_number
            ''', user_id, first_name, last_name, phone_number)

        await message.reply("Спасибо за предоставленный номер телефона!")

    def run(self):
        executor.start_polling(self.dp, skip_updates=True)


if __name__ == '__main__':
    # Инициализация логирования
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("error.log"),
            logging.StreamHandler()
        ]
    )

    bot_handler = BotHandler()
    bot_handler.run()
