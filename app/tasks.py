import os
from datetime import datetime

from sqlalchemy import select
from aiogram import Bot
from sqlalchemy.orm import selectinload

from app.db import AsyncSessionLocal
from app.models import Battle
from app.utils.time import get_nearest_day


WEBHOOK_URL = os.getenv('WEBHOOK_URL')


async def send_battle_notification(bot: Bot):
    now = datetime.now()
    hour = 10
    day = get_nearest_day()
    if now.hour >= 10 and now.hour < 22:
        hour = now.hour + 3
        day = now.date()
    async with AsyncSessionLocal() as session:
        result = await session.scalar(
            select(Battle)
            .options(selectinload(Battle.for_user))
            .where(Battle.date == day, Battle.hour == hour)
        )
        if result is None or result.for_user is None:
            username = None
        else:
            username = result.for_user.username
    if username is None:
        await bot.send_message(-1001598872748, f'Стоило бы занять битву.')
    await bot.send_message(-1001598872748, f'Привет, @{username}.')


async def on_startup(bot: Bot):
    await bot.delete_webhook(True)
    await bot.set_webhook(WEBHOOK_URL, secret_token=bot['super_secret'])
