import logging
from typing import Tuple, Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageNotModified
from modules.database.models import Answer, Question, Survey, User, find_user
from modules.surveys import messages, config


async def start_survey(user: User, survey: Survey, message_from_user: types.Message, start_number=0):
    '''
    Starts `survey` for `user`.
    '''
    amount_of_questions = survey.questions.__len__()
    assert amount_of_questions > 0, survey

    user.update(
        current_survey=survey.raw_data,
        current_question_number=start_number,
        answers=[[] for _ in range(amount_of_questions)],
    )
    message = await message_from_user.answer('_')
    await show_question(user, user.current_question_number, message=message)


async def show_question(user: User, question_number: int, message: types.Message) -> Union[Question, None]:
    '''
    Edit `message` with actual question
    Returns question if question_number is valid
    '''
    survey = Survey(**user.current_survey)
    question = None
    N = survey.questions.__len__()
    # If there is such question in survey
    if 0 <= question_number < N:
        question = survey.questions[question_number]
        assert question.number == question_number
        user.update(
            current_question_number=question_number
        )
        text, keyboard = represent_question(user, question)
    # If questions are over
    elif question_number >= N:
        text = 'There is no questions'
        keyboard = get_submit_keyboard(survey)
    # Question number are negative. Something is wrong
    else:
        text, keyboard = 'None', None

    if message.text != text:
        await message.edit_text(text)

    try:
        await message.edit_reply_markup(keyboard)
    except MessageNotModified:
        logging.error(
            f"message not modified. q_num: {question_number} user: {user}")

    return question


def represent_question(user: User, question: Question) -> Tuple[str, types.InlineKeyboardMarkup]:
    '''
    Returns text of message and button for telegram message
    '''

    answer = user.answers[question.number]
    keyboard = get_question_keyboard(question, answer)
    text = question.__str__()

    # input text workaround
    if question.type == 3 and answer:
        text += f'Your current answer:\n"{answer[0]}"'

    return text, keyboard


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


async def process_plain_text(message: types.Message, state: FSMContext):
    user = find_user(chat_id=message.chat.id)
    if not user:
        return

    answer_text = message.text

    if len(answer_text) > config.PLAIN_TEXT_MAX_LENGTH:
        await message.answer(messages.PROCEES_PLAIN_TEXT_MAX_LENGTH % config.PLAIN_TEXT_MAX_LENGTH)
        return

    cur_number = user.current_question_number
    user.answers[cur_number] = [answer_text]
    user.commit()

    await message.answer(messages.PROCESS_PLAIN_TEXT_OK)
    message = await message.answer('_')
    await show_question(user, cur_number, message=message)
