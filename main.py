import asyncio
from os import getenv

from aiogram import Bot, Dispatcher
from database import init_db
from dotenv import load_dotenv

from handleres.common import comm
from handleres.files import file
from handleres.payments import pay
from handleres.registration import registration

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_routers(registration, pay, file, comm)


async def main():
    bot = Bot(token=TOKEN)
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
