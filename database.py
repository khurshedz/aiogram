import asyncpg
import config
import logging

class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def connect(self):
        try:
            self.pool = await asyncpg.create_pool(
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                database=config.POSTGRES_DB,
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT
            )
            logging.info("Connected to database")
        except Exception as e:
            logging.error(f"Error connecting to database: {e}")

    async def save_contact(self, user_id, first_name, last_name, phone_number):
        try:
            async with self.pool.acquire() as connection:
                await connection.execute('''
                    INSERT INTO contacts (user_id, first_name, last_name, phone_number) VALUES ($1, $2, $3, $4)
                    ON CONFLICT (user_id) DO UPDATE SET phone_number = EXCLUDED.phone_number
                ''', user_id, first_name, last_name, phone_number)
            logging.info(f"Saved contact for user {user_id}")
        except Exception as e:
            logging.error(f"Error saving contact: {e}")
