from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, StateFilter
import logging

from .start import cmd_start
from .register import cmd_register, RegistrationStates, process_code, process_email
from .unregister import cmd_unregister
from .info import cmd_info
from .callback_functions import callback_answer_handler, callback_survey_handler

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

    # info
    dp.register_message_handler(cmd_info, Command('info'), state='*')

    # answer handler
    dp.register_callback_query_handler(
        callback_answer_handler,
        lambda query: query.data.startswith('answer'),
    )
    # submit handler
    dp.register_callback_query_handler(
        callback_survey_handler,
        lambda query: query.data.startswith('survey'),
    )