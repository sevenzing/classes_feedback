from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram import types
import logging

from modules.surveys.server_communation import validate_user
from modules.common.utils import parse_command, is_email_correct
from modules.database.models import (
    Track,
    User, 
    find_user,
    create_user,
    )
    
from . import messages

class RegistrationStates(StatesGroup):
    wait_for_email = State()
    wait_for_code = State()


async def cmd_register(message: types.Message):
    logging.debug(f"register message. {message.from_user.id}/{message.from_user.username}")
    user = find_user(chat_id=message.from_user.id)
    if user:
        await message.answer(messages.REGISTERED)
    else:
        await RegistrationStates.wait_for_email.set()
        await message.answer(messages.SEND_EMAIL)


async def process_email(message: types.Message, state: FSMContext):
    '''
    Executes only if state is wait_for_email.
    Process email from user
    '''
    email = message.text
    if not is_email_correct(email):
        await message.answer(messages.INVALID_EMAIL)
        return
        
    async with state.proxy() as data:
        data['email'] = email
    
    await RegistrationStates.next()
    await message.answer(messages.SEND_CODE)

async def process_code(message: types.Message, state: FSMContext):
    '''
    Executes only if state is wait_for_code.
    Validates code from user
    '''
    code: str = message.text
    if not code.isdigit():
        await message.answer(messages.INVALID_CODE)
        return

    async with state.proxy() as data:
        email = data['email']
    
    user_response = validate_user(email, code)
    if not user_response['confirmed']:    
        await message.answer(messages.INVALID_CODE)
    else:
        # create user
        chat_id = message.from_user.id
        username = message.from_user.username
        track = Track(**user_response['track'])
        try:
            user = create_user(chat_id, email, username, track.raw_data)
        except Exception:
            await message.answer('error.')
            return
        finally:    
            await state.finish()
        
        await message.answer(messages.REGISTER_FINISH % (email, track))
