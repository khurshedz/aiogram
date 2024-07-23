import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TELEGRAM_API_TOKEN
from database.db import init_db
from handlers import start_handler, contact_handler, loan_handler, problem_handler, refinance_handler

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("error.log"),
        logging.StreamHandler()
    ]
)

async def on_startup(dispatcher):
    # Initialize database
    dispatcher['db_pool'] = await init_db()

async def on_shutdown(dispatcher):
    await dispatcher['db_pool'].close()

def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())

    # Register handlers
    dp.register_message_handler(start_handler.send_welcome, commands=['start', 'help'])
    dp.register_message_handler(contact_handler.handle_contact, content_types=['contact'], state='*')
    dp.register_message_handler(loan_handler.handle_loan, text='📋 Хочу взять займ', state='*')
    dp.register_message_handler(problem_handler.handle_problem, text='✏ Есть проблема или вопрос', state='*')
    dp.register_message_handler(refinance_handler.handle_refinance, text='✂ Хочу рефинансировать займ', state='*')

    # Register state-specific handlers
    dp.register_message_handler(loan_handler.loan_choice, state=loan_handler.Form.loan_choice)
    # dp.register_message_handler(loan_handler.online_application, state=loan_handler.Form.online_application)
    # dp.register_message_handler(loan_handler.offline_application, state=loan_handler.Form.offline_application)
    # dp.register_message_handler(loan_handler.personal_loan, state=loan_handler.Form.personal_loan)
    # dp.register_message_handler(loan_handler.mortgage, state=loan_handler.Form.mortgage)
    # dp.register_message_handler(loan_handler.consumer_loan, state=loan_handler.Form.consumer_loan)
    # dp.register_message_handler(loan_handler.date_choice, state=loan_handler.Form.date_choice)
    # dp.register_message_handler(loan_handler.success, state=loan_handler.Form.success)
    #
    # dp.register_message_handler(problem_handler.problem_choice, state=problem_handler.ProblemForm.problem_choice)
    # dp.register_message_handler(refinance_handler.refinance_choice, state=refinance_handler.RefinanceForm.refinance_choice)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("error.log"),
            logging.StreamHandler()
        ]
    )
    main()
