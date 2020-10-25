from aiogram import types
import logging

from modules.surveys.server_communation import validate_user
from modules.database.models import User, find_user, create_user
from modules.common.utils import parse_command, is_email_correct
from . import messages


async def cmd_unregister(message: types.Message):
    logging.debug(f"unregister message. {message.from_user.id}/{message.from_user.username}")
    chat_id = message.from_user.id
    user = find_user(chat_id=chat_id)
    if not user:
        await message.answer('You are not registered')
        return
    else:
        if user.delete():
            await message.answer('removed')

