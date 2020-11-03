from aiogram import types
from modules.database.models import Survey, User, Track, find_user
from modules.surveys.question_manager import show_question
from . import messages
import logging


async def callback_answer_handler(query: types.CallbackQuery):
    '''
    Callback for question button
    '''
    user = find_user(chat_id=query.message.chat.id)
    if not user:
        return
    
    _, command, question_number, choice_number = query.data.split(':')
    
    if command == messages.COMMAND_SET:
        question_number = int(question_number)
        question = Survey(**user.current_survey).questions[question_number]
        
        # delete
        if choice_number in user.answers[question_number]:
            user.answers[question_number].remove(choice_number)
        
        # add/change
        else:
            if question.type == 0:
                user.answers[question_number] = [choice_number]
            elif question.type == 1:
                user.answers[question_number].append(choice_number)
            else:
                logging.warning('pizda')
        user.commit()
        await show_question(user, question_number, query.message)

    elif command == messages.COMMAND_CHANGE:
        await show_question(user, int(choice_number), query.message)
    
    await query.answer('')
    

async def callback_survey_handler(query: types.CallbackQuery):
    user = find_user(chat_id=query.message.chat.id)
    if not user:
        return
    
    _, command, question_number, choice_number = query.data.split(':')

    if command == messages.COMMAND_SUBMIT:
        await query.answer('submitted')
        await query.message.delete()
    
    await query.answer('')