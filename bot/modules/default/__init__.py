from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
from asyncio import AbstractEventLoop
import logging

from .cancel import cmd_cancel
from .help import cmd_help
from .callback_empty_button import answer_callback_empty_button_handler


def setup(dp: Dispatcher, loop: AbstractEventLoop=None, *args, **kwargs):
    logging.info('Initialize default module')
    
    dp.register_message_handler(cmd_help, Command('help'), state='*')
    dp.register_message_handler(cmd_cancel, Command('cancel'), state='*')
    dp.register_callback_query_handler(
        answer_callback_empty_button_handler,
        lambda query: query.data == 'None'
    )