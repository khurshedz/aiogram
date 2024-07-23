from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.loan_keyboards import get_loan_keyboard, get_online_application_keyboard, \
    get_offline_application_keyboard


class Form(StatesGroup):
    loan_choice = State()
    online_application = State()
    offline_application = State()
    personal_loan = State()
    mortgage = State()
    consumer_loan = State()
    date_choice = State()
    success = State()


async def handle_loan(message: types.Message, state: FSMContext):
    await Form.loan_choice.set()
    await message.reply("Какой вид займа вас интересует?", reply_markup=get_loan_keyboard())


async def loan_choice(message: types.Message, state: FSMContext):
    if message.text == 'Онлайн':
        await Form.online_application.set()
        await message.reply("Вы выбрали онлайн-заявку. Что бы вы хотели сделать?",
                            reply_markup=get_online_application_keyboard())
    elif message.text == 'Офлайн':
        await Form.offline_application.set()
        await message.reply("Вы выбрали офлайн-заявку. Что бы вы хотели сделать?",
                            reply_markup=get_offline_application_keyboard())
    else:
        await message.reply("Пожалуйста, выберите один из предложенных вариантов.")
