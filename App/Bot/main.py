import asyncio
from aiogram import Bot, Dispatcher, F

from os import getenv
from dotenv import load_dotenv

from App.Bot.handlers import basic


dp = Dispatcher()

load_dotenv()
TOKEN = getenv("BOT_TOKEN")
bot = Bot(TOKEN)


async def start():

    try:
        dp.include_routers(
            basic.router
        )
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())
