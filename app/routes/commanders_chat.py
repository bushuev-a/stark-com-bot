from datetime import date, datetime, timedelta

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload
from babel.dates import format_date

from app.models import Battle, User
from app.db import AsyncSessionLocal
from app.utils.time import get_nearest_day

commanders_chat_router = Router()

# commanders_chat_router.message.filter(F.chat.id.in_([]))


async def get_battles(day: date):
    data = [
        {'hour': hour, 'date': day} for hour in [10, 13, 16, 19, 22]
    ]
    stmt = insert(Battle)
    on_conflict_stmt = stmt.on_conflict_do_nothing(
        index_elements=['hour', 'date']
    )
    async with AsyncSessionLocal() as session:
        await session.execute(on_conflict_stmt, data)
        await session.commit()
        results = await session.scalars(
            select(Battle)
            .options(selectinload(Battle.for_user))
            .where(Battle.date == day)
            .order_by(Battle.hour)
        )
    return results


def render_schedule(battles):
    schedule = []
    builder = InlineKeyboardBuilder()
    day = None
    for battle in battles:
        day = battle.date
        if battle.for_user is not None:
            user = battle.for_user.name
        else:
            user = 'пусто'
        schedule.append(f'{battle.hour}:00 - {user}')
        builder.button(text=f'{battle.hour}', callback_data=f"schedule:{battle.id}")
    # builder.adjust(3)
    schedule_text = '\n'.join(schedule)
    date_string = format_date(day, locale='ru_RU')
    return f'#расписание на {date_string}\n{schedule_text}', builder.as_markup()


@commanders_chat_router.message(Command('schedule'))
async def schedule_handler(message: Message):
    battles = await get_battles(get_nearest_day())
    text, markup = render_schedule(battles)
    await message.answer(text, reply_markup=markup)


@commanders_chat_router.callback_query(F.data.regexp(r"schedule:(?P<id>\d+)").as_('match'))
async def on_schedule_select(callback_query: CallbackQuery, match):
    battle_id = int(match.group('id'))
    user_id = callback_query.from_user.id
    async with AsyncSessionLocal() as session:
        battle = await session.get_one(Battle, battle_id)
        if battle.for_user_id == user_id:
            battle.for_user_id = None
        else:
            battle.for_user_id = user_id
        day = battle.date
        await session.commit()

    battles = await get_battles(day)
    text, markup = render_schedule(battles)
    await callback_query.message.edit_text(text, reply_markup=markup)
    await callback_query.answer()
