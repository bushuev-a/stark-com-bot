from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from app.db import AsyncSessionLocal
from app.models import User

private_router = Router()

private_router.message.filter(F.chat.type == 'private')


@private_router.message(Command('start'))
async def start_handler(message: Message):
    user: User = User(
        id=message.from_user.id,
        name=message.from_user.full_name,
        username=message.from_user.username
    )
    async with AsyncSessionLocal() as session:
        await session.merge(user)
        await session.commit()
    await message.answer('Hi!')
