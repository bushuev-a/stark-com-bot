from datetime import datetime

from sqlalchemy import select
from aiogram import Bot
from sqlalchemy.orm import selectinload

from app.db import AsyncSessionLocal
from app.models import Battle
from app.utils.time import get_nearest_day


async def send_battle_notification(bot: Bot):
    now = datetime.now()
    hour = 10
    if now.hour >= 10 and now.hour < 22:
        hour = now.hour + 3
    async with AsyncSessionLocal() as session:
        result = await session.scalar(
            select(Battle)
            .options(selectinload(Battle.for_user))
            .where(Battle.date == get_nearest_day(), Battle.hour == hour)
        )
        if result is None or result.for_user is None:
            username = None
        else:
            username = result.for_user.username
    if username is None:
        await bot.send_message(-1001598872748, f'Стоило бы занять битву.')
    await bot.send_message(-1001598872748, f'Привет, @{username}.')
