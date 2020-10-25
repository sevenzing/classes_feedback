from aiogram import types
import logging

from modules.surveys.server_communation import get_survey, Survey
from modules.database.models import User, Track, find_user
from modules.common.utils import parse_command
from . import messages


async def cmd_start(message: types.Message):
    '''
    Conversation's entry point. Send start message
    '''
    logging.debug(f"start message. {message.from_user.id}/{message.from_user.username}")
    _, args = parse_command(message.text)
    
    if args:
        chat_id = message.chat.id
        pk = args[0]
        user: User = find_user(chat_id=chat_id)
        logging.debug(f"user: {user}")
        
        if not user:
            await message.answer(messages.NOT_REGISTERED)
            return
    
        survey = await get_survey_or_none(user, pk)
        if survey:
            await message.answer(survey.__str__())
        else:
            await message.answer(messages.HAVE_NO_PERMISSION)
    else:
        await message.answer(messages.ON_CMD_START)

async def get_survey_or_none(user: User, pk):
    survey: Survey = get_survey(pk)
    if not survey:
        return
    
    survey_track = survey.course.track
    
    if survey_track == Track(**user.track):
        return survey
    else:
        logging.debug(f'User {user} have not access to track {survey_track}')
    