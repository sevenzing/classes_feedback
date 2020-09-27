from aiogram import types


async def answer_callback_empty_button_handler(query: types.CallbackQuery):
    '''
    Callback for empty button
    '''
    await query.answer(text='')