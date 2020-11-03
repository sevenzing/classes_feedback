from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
import logging

from .start import cmd_start
from .register import cmd_register, RegistrationStates, process_code, process_email
from .unregister import cmd_unregister

def setup(dp: Dispatcher, *args, **kwargs):
    logging.info('Initialize surveys module')
    
    # getting survey
    dp.register_message_handler(cmd_start, Command('start'), state='*')
    
    # registration
    dp.register_message_handler(cmd_register, Command('register'), state='*')
    dp.register_message_handler(process_email, state=RegistrationStates.wait_for_email)
    dp.register_message_handler(process_code, state=RegistrationStates.wait_for_code)

    # unregister
    dp.register_message_handler(cmd_unregister, Command('unregister'), state='*')