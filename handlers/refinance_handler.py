from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class RefinanceForm(StatesGroup):
    refinance_choice = State()


async def handle_refinance(message: types.Message):
    await RefinanceForm.refinance_choice.set()
    await message.reply("Какой вид рефинансирования вас интересует?", reply_markup=get_refinance_keyboard())


async def get_refinance_keyboard(message: types.Message):
    # текст """Пожалуйста свяжитесь с нами по номеру 88009556699""" показать кнопку позвонить, которая направляет в телефон
    # назад в гл меню
    pass
