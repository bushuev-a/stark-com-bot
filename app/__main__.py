import os
import asyncio
import logging

import aiocron
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

from app.tasks import send_battle_notification
from app.routes.private import private_router
from app.routes.commanders_chat import commanders_chat_router

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_routers(
    private_router,
    commanders_chat_router
)


@aiocron.crontab('1 10,13,16,19,22 * * *', loop=loop)
async def after_battle():
    await send_battle_notification(bot)


async def main():
    # await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    loop.run_until_complete(main())
