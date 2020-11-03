from modules.database.models import Survey, User, Question, Answer
from aiogram import types
from aiogram.utils.exceptions import MessageNotModified
from typing import Tuple
import logging

async def start_survey(user: User, survey: Survey, message_from_user: types.Message):
    amount_of_questions = survey.questions.__len__()
    assert amount_of_questions > 0, survey
    
    user.update(
        current_survey=survey.raw_data,
        current_question_number=0,
        answers=[{}] * amount_of_questions,
    )
    message = await message_from_user.answer('_')
    await show_question(user, user.current_question_number, message=message)

async def show_question(user: User, question_number: int, message: types.Message):
    question = Survey(**user.current_survey).questions[question_number]
    assert question.number == question_number
    text, keyboard = represent_question(user, question)
    await message.edit_text(text)
    try:
        await message.edit_reply_markup(keyboard)
    except MessageNotModified:
        logging.error(f"message not modified. q_num: {question_number} user: {user}")

def represent_question(user: User, question: Question) -> Tuple[str, types.InlineKeyboardMarkup]:
    answer = Answer(**(user.answers[question.number] or {}))
    keyboard = get_keyboard(question, answer)
    return question.__str__(), keyboard

def get_keyboard(question: Question, answer) -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    question_number = question.number
    
    # Single and multi choice
    if question.type in [0, 1]:    
        for choice_number, choice in enumerate(question.data):
            keyboard.add(
                types.InlineKeyboardButton(
                    text=f"{choice_number}: {choice}",
                    callback_data=f"answer:set:{question_number}:{choice_number}",
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
    
    return keyboard