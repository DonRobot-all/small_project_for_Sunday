import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram import F
import logging
import sqlite3

TOKEN = ''

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


conn = sqlite3.connect('chat.db')
cursor = conn.cursor()

async def save_message(user: str, text: str):
    print(user, text)
    cursor.executemany("INSERT INTO messages (user, message) VALUES (?, ?)", [(user, text)])
    conn.commit()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Привет! Напиши мне сообщение, и я его сохраню в чат.")


@dp.message(F.text)
async def message_handler(message: Message):
    username = message.from_user.username or f"id{message.from_user.id}"
    text = message.text
    await save_message(username, text)
    await message.answer(f"Сообщение сохранено: <b>{text}</b>")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
