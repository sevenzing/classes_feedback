from aiogram import types
import functools
import logging

from misc import bot
from modules.common.config import constants


def admin_only_handler(func):
    '''
    Decorate handler function to be admin only  
    '''
    @functools.wraps(func)
    async def call(message: types.Message, *args, **kwargs):
        logging.info(f"User {message.from_user.id}/{message.from_user.username} is trying to execute admin command")
        if message.from_user.id == constants.BOT_ADMIN:
            return await func(message, *args, **kwargs)
    return call


async def send_message_to_admin(text) -> types.Message:
    logging.debug('Send message to admin')
    return await bot.send_message(constants.BOT_ADMIN, text)
    
        