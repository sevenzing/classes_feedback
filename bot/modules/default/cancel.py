from aiogram import types
from aiogram.dispatcher import FSMContext
from modules.default import messages

import logging


async def cmd_cancel(message: types.Message, state: FSMContext):
    '''
    Allow user to cancel any action
    '''
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.debug(f"Cancelling state {current_state} for chat {message.chat.id}")

    await state.finish()

    await message.answer(messages.ON_CMD_CANCEL, reply_markup=types.ReplyKeyboardRemove())
