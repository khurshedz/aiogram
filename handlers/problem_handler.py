from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class ProblemForm(StatesGroup):
    problem_choice = State()


async def handle_problem(message: types.Message):
    await ProblemForm.problem_choice.set()
    await message.reply("Какую проблему вы хотите решить?", reply_markup=get_problem_keyboard())


async def get_problem_keyboard(message: types.Message):
    # Получить текст сообщения из handle_probplem и отрпавить по почте
    pass