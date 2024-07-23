from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.loan_keyboards import get_main_keyboard


async def send_welcome(message: types.Message, state: FSMContext):
    welcome_text = (
        "Я — бот Деньга. Помогу:\n"
        "1️⃣ Выбрать и оформить займ\n"
        "2️⃣ Рефинансировать старый займ\n"
        "3️⃣ Связаться с нужным специалистом\n"
    )
    await state.finish()  # Сброс всех состояний
    await message.reply(welcome_text, reply_markup=get_main_keyboard())
