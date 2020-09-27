from aiogram import types
import logging

from modules.default import messages
from modules.database.models.user import User, get_user, create_user_if_not_exists
from modules.database import db_handler

@db_handler(commit=True)
async def cmd_start(session, message: types.Message):
    '''
    Conversation's entry point. Send start message
    '''
    chat_id = message.chat.id
    user: User = create_user_if_not_exists(chat_id=chat_id)
    user.update(username=message.from_user.username)
    logging.info(f"user created: {get_user(chat_id=chat_id)}")
    await message.answer(messages.ON_CMD_START)
