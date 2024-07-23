from aiogram import types
import logging
from aiogram.dispatcher import FSMContext

async def handle_contact(message: types.Message, state: FSMContext, pool):
    contact = message.contact
    phone_number = contact.phone_number
    user_id = contact.user_id
    first_name = contact.first_name
    last_name = contact.last_name

    # Логируем номер телефона и пользователя
    logging.info(f"User ID: {user_id}, First Name: {first_name}, Last Name: {last_name}, Phone Number: {phone_number}")

    # Сохраняем контакт в базу данных
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO contacts (user_id, first_name, last_name, phone_number) VALUES ($1, $2, $3, $4)
            ON CONFLICT (user_id) DO UPDATE SET phone_number = EXCLUDED.phone_number
        ''', user_id, first_name, last_name, phone_number)

    await message.reply("Спасибо за предоставленный номер телефона!")
    await state.finish()
