import os
from aiogram import Router, Bot, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from config import DATA_PATH

router = Router()


@router.message(Command("list"))
async def send_files_list(message: Message):
    list_dir = os.listdir(DATA_PATH)

    await message.answer(str(list_dir))


@router.message(F.document)
async def get_file(message: Message, bot: Bot):
    file_id = message.document.file_id
    file_name = message.document.file_name

    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, f"{DATA_PATH}/{file_name}")


@router.message(Command("get"))
async def get_by_name(message: Message):
    text = message.text
    text = text.split()
    filename = text[1]
    file_path = DATA_PATH / filename

    if file_path.exists():
        file = FSInputFile(file_path)
        await message.answer_document(file)

@router.message(Command("get_all"))
async def get_by_name(message: Message):
    for f in os.listdir(DATA_PATH):
        file = FSInputFile(DATA_PATH / f)
        await message.answer_document(file)

