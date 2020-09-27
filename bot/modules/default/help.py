from aiogram import types

from modules.default import messages


async def cmd_help(message: types.Message):
    '''
    Send help message
    '''
    await message.answer(messages.ON_CMD_HELP, parse_mode='Markdown')