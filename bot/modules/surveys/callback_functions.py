import logging
from typing import Union

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from modules.database.models import Survey, Track, Question, User, find_user
from modules.surveys import messages
from modules.surveys.question_manager import show_question
from modules.surveys.server_communation import post_answer

class QuestionsStates(StatesGroup):
    wait_for_plain_text = State()


async def callback_answer_handler(query: types.CallbackQuery, state: FSMContext):
    '''
    Callback for question button
    '''
    user = find_user(chat_id=query.message.chat.id)
    if not user:
        return

    await state.finish()
    
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
                logging.warning(
                    f"There is no such question type as {question.type}"
                )
        user.commit()
        await show_question(user, question_number, query.message)

    elif command == messages.COMMAND_CHANGE:
        new_question: Union[Question, None] = await show_question(user, int(choice_number), query.message)
        if new_question:
            if new_question.type == 3:
                await QuestionsStates.wait_for_plain_text.set()
            else:
                pass

    await query.answer('')


async def callback_survey_handler(query: types.CallbackQuery):
    user = find_user(chat_id=query.message.chat.id)
    if not user:
        return

    _, command, question_number, choice_number = query.data.split(':')
    survey = Survey(**user.current_survey)
    raw_answers = user.answers
    questions = survey.questions
    
    if command == messages.COMMAND_SUBMIT:
        answers = list(map(
            lambda x: {'answer_data': x[0], 'question_id':x[1].id}, 
            zip(raw_answers, questions))
            )
        logging.debug(f"{answers}")
        
        # post all answers to the server
        for answer in answers:
            post_answer(**answer)
        
        await query.answer('submitted')
        await query.message.delete()
    else:
        logging.warning(f"There is no such command as {command}. query: {query.data}")
    await query.answer('')
