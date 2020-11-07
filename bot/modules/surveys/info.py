import logging

from aiogram import types
from modules.database.models import Track, User, find_user
from modules.surveys import messages


async def cmd_info(message: types.Message):
    logging.debug(
        f"info message. {message.from_user.id}/{message.from_user.username}")
    chat_id = message.from_user.id
    user = find_user(chat_id=chat_id)
    if not user:
        await message.answer('You are not registered')
        return
    else:
        await message.answer(f"email: {user.email}\nTrack: {Track(**user.track)}")
