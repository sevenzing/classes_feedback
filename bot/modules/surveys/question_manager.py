from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from typing import Tuple
from modules.database.models import Survey, User, Question, Answer
import logging

from . import messages


async def start_survey(user: User, survey: Survey, message_from_user: types.Message):
    '''
    Starts `survey` for `user`.
    '''
    amount_of_questions = survey.questions.__len__()
    assert amount_of_questions > 0, survey
    
    user.update(
        current_survey=survey.raw_data,
        current_question_number=0,
        answers=[[] for _ in range(amount_of_questions)],
    )
    message = await message_from_user.answer('_')
    await show_question(user, user.current_question_number, message=message)

async def show_question(user: User, question_number: int, message: types.Message):
    '''
    Edit `message` with actual question
    '''
    survey = Survey(**user.current_survey)
    N = survey.questions.__len__()
    if 0 <= question_number < N:
        question = survey.questions[question_number]
        assert question.number == question_number
        text, keyboard = represent_question(user, question)

    elif question_number >= N:
        text = 'There is no questions'
        keyboard = get_submit_keyboard(survey)
    else:
        text, keyboard = 'None', None

    if message.text != text:
            await message.edit_text(text)
        
    try:
        await message.edit_reply_markup(keyboard)
    except MessageNotModified:
        logging.error(f"message not modified. q_num: {question_number} user: {user}")

def represent_question(user: User, question: Question) -> Tuple[str, types.InlineKeyboardMarkup]:
    '''
    Returns text of message and button for telegram message
    '''

    answer = user.answers[question.number]
    keyboard = get_question_keyboard(question, answer)
    return question.__str__(), keyboard

def get_question_keyboard(question: Question, answer: list) -> types.InlineKeyboardMarkup:
    '''
    Return buttons for choosing answer in this way:
    [1: ... ] 
    [2: ... ]
    [3: ... ] 
    [4: ... ]
    
       ...
       
    [ PREV ]
    [ NEXT ]
    '''
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    question_number = question.number
    
    # Single and multi choice
    if question.type in [0, 1]:    
        for choice_number, choice in enumerate(question.data):
            logging.warning(f"{choice}, {choice_number}, {answer}")
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f"{messages.SELECTED if str(choice_number) in answer else messages.NOT_SELECTED} {choice_number}: {choice}",
                    callback_data=f"answer:{messages.COMMAND_SET}:{question_number}:{choice_number}",
                )
            )
    # Rate question
    elif question.type == 2:
        pass
    # Input text
    elif question.type == 3:
        pass
    else:
        pass
    
    if question_number > 0:
        keyboard.add(
            types.InlineKeyboardButton(
                        text=f"PREV",
                        callback_data=f"answer:{messages.COMMAND_CHANGE}:{question_number}:{question_number - 1}",
                    )
                )
    if question_number < question.N:
        keyboard.add(
            types.InlineKeyboardButton(
                        text=f"NEXT",
                        callback_data=f"answer:{messages.COMMAND_CHANGE}:{question_number}:{question_number + 1}",
                    )
                )
    
    return keyboard

def get_submit_keyboard(survey: Survey) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    
    keyboard.add(
            types.InlineKeyboardButton(
                        text=f"GO TO 1ST QUESTION",
                        callback_data=f"answer:{messages.COMMAND_CHANGE}:None:0",
                    )
                )
    
    keyboard.add(
            types.InlineKeyboardButton(
                        text=f"SUBMIT",
                        callback_data=f"survey:{messages.COMMAND_SUBMIT}:{survey.id}:",
                    )
                )
    
    return keyboard