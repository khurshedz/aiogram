import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import config
from database import DatabaseManager
from keyboards import Keyboards
from handlers import Handlers


class BotHandler:
    def __init__(self):
        self.bot = Bot(token=config.TELEGRAM_API_TOKEN)
        self.dp = Dispatcher(self.bot)
        self.dp.middleware.setup(LoggingMiddleware())

        # Инициализация базы данных
        self.db_manager = DatabaseManager()
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.init_db())

        # Инициализация клавиатуры и обработчиков
        self.keyboards = Keyboards()
        self.handlers = Handlers(self.dp, self.db_manager, self.keyboards)

    async def init_db(self):
        await self.db_manager.connect()

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
