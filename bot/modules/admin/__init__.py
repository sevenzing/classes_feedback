import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from .uptime import cmd_uptime


def setup(dp: Dispatcher, *args, **kwargs):
    logging.info('Initialize admin module')
    
    dp.register_message_handler(cmd_uptime, Command('uptime', prefixes='#'))
