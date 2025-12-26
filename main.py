import asyncio
from aiogram import Dispatcher, Bot, F
from aiogram.types import FSInputFile, Message
from aiogram.filters import Command
import os
from pathlib import Path

BOT_TOKEN = "...."
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DATA_PATH = Path(__file__).parent / "data"

if not DATA_PATH.exists():
    DATA_PATH.mkdir()


@dp.message(Command("list"))
async def send_files_list(message: Message):
    list_dir = os.listdir(DATA_PATH)

    await message.answer(str(list_dir))


@dp.message(F.document)
async def det_file(message: Message, bot: Bot):
    file_id = message.document.file_id
    file_name = message.document.file_name

    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, f"{DATA_PATH}/{file_name}")


@dp.message(Command("get"))
async def get_by_name(message: Message):
    text = message.text
    text = text.split()
    filename = text[1]
    file_path = DATA_PATH / filename

    if file_path.exists():
        file = FSInputFile(file_path)
        await message.answer_document(file)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
