import logging

from aiogram import types
from modules.database.models import find_user
from modules.surveys import messages


async def cmd_unregister(message: types.Message):
    logging.debug(
        f"unregister message. {message.from_user.id}/{message.from_user.username}")
    chat_id = message.from_user.id
    user = find_user(chat_id=chat_id)
    if not user:
        await message.answer('You are not registered')
        return
    else:
        if user.delete():
            await message.answer('removed')
