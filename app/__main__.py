import os
import asyncio
import logging

import aiocron
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

from app.http.gpt_get_schedule import http_get_schedule
from app.tasks import send_battle_notification, on_startup
from app.routes.private import private_router
from app.routes.commanders_chat import commanders_chat_router

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()
BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = web.Application()

dp.startup.register(on_startup)
dp.include_routers(
    private_router,
    commanders_chat_router
)


@aiocron.crontab('1 10,13,16,19,22 * * *', loop=loop)
async def after_battle():
    await send_battle_notification(bot)


def main():
    # await bot.delete_webhook(True)
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=BOT_TOKEN,
    )
    # Register webhook handler on application
    webhook_requests_handler.register(app, path='/webhook')

    # Mount dispatcher startup and shutdown hooks to aiohttp application
    setup_application(app, dp, bot=bot)
    web.get('/my-gpt/schedule', http_get_schedule)
    web.run_app(app, port=8006, loop=loop)


if __name__ == '__main__':
    main()
