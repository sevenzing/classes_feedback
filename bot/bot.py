from aiogram import executor
import logging

from misc import dp
from modules.default import setup as setup_default
from modules.surveys import setup as setup_surveys
from modules.admin import setup as setup_admin
from modules.admin.utils import send_message_to_admin
import modules.database.models

async def on_startup(dp):
    await send_message_to_admin('Starting the bot')

async def on_shutdown(dp):
    await send_message_to_admin('Shut down the bot')


if __name__ == '__main__':
    setup_default(dp)
    setup_surveys(dp)
    setup_admin(dp)
    
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
