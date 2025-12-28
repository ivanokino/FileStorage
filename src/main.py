import asyncio
from aiogram import Dispatcher, Bot

from handlers import router
from config import BOT_TOKEN, DATA_PATH


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

if not DATA_PATH.exists():
    DATA_PATH.mkdir()

dp.include_router(router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
