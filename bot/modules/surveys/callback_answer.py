from aiogram import types


async def callback_answer_handler(query: types.CallbackQuery):
    '''
    Callback for question button
    '''

    await query.answer(text=query.data)