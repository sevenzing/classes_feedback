from aiogram import types

from modules.surveys.server_communation import get_survey
from modules.surveys.question_manager import start_survey
from modules.database.models import Survey, User, Track, find_user
from modules.common.utils import parse_command
from modules.surveys import messages

import logging


async def cmd_start(message: types.Message):
    '''
    Conversation's entry point. Send start message
    '''
    logging.debug(f"start message. {message.from_user.id}/{message.from_user.username}")
    _, args = parse_command(message.text)
    
    if args:
        chat_id = message.chat.id
        pk = args[0]
        user = find_user(chat_id=chat_id)
        logging.debug(f"user: {user}")
        
        if not user:
            await message.answer(messages.NOT_REGISTERED)
            return

        try:
            survey = get_survey_or_error(user, pk)
        except (AccessError, DeadlineError) as e:
            await message.answer(e.__str__())
            return
            
        if survey:
            # TODO: survey representation
            await start_survey(user, survey, message)
            
            #await message.answer(survey.__str__())
        else:
            await message.answer(messages.HAVE_NO_PERMISSION)
    else:
        await message.answer(messages.ON_CMD_START)

class AccessError(Exception):
    pass

class DeadlineError(Exception):
    pass

def get_survey_or_error(user: User, pk):
    survey: Survey = get_survey(pk)
    if not survey:
        raise AccessError("You don't have access to this survey")
    
    survey_track = survey.course.track
    if survey_track != Track(**user.track):
        logging.debug(f'User {user} have not access to track {survey_track}')
        raise AccessError("You don't have access to this survey")
    
    elif not survey.is_available:
        logging.debug(f'User {user} has access to track, but deadline is gone')
        raise DeadlineError("The survey deadline has expired")
    
    else:
        return survey