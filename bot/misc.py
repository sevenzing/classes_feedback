from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from pymongo import MongoClient
from umongo import Instance
import logging

from modules.common.config import constants


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -15s %(funcName) -20s: %(message)s')
LOG_LEVEL = logging.DEBUG if constants.LOG_LEVEL == 'debug' else logging.INFO if constants.LOG_LEVEL == 'info' else logging.ERROR
logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)

storage = RedisStorage2(**constants.redis)

mongo_client = MongoClient(**constants.mongo)
mongo_instance = Instance(mongo_client.surveys)

bot = Bot(token=constants.BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


