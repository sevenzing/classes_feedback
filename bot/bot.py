from aiogram import executor
import logging

from misc import dp, Base, db_engine
from modules.default import setup as setup_default
from modules.admin import setup as setup_admin
from modules.admin.utils import send_message_to_admin
import modules.database.models

async def on_startup(dp):
    await send_message_to_admin('Starting the bot')

async def on_shutdown(dp):
    await send_message_to_admin('Shut down the bot')

from modules.database.models import User

if __name__ == '__main__':
    logging.info(User.__table__)
    setup_default(dp)
    setup_admin(dp)
    
    Base.metadata.create_all(db_engine)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
