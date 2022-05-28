from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import pytz

from modules import database as db

credentials = yaml.load(open('./modules/data/credentials.yaml'), Loader=yaml.FullLoader)
user_template = {
    'lang': 'en',
    'currency_pair': None,
    'up_interval': None,
    'tracking_job_id': None
}

storage = MemoryStorage()
bot = Bot(token=credentials['telegram']['bot']['token'])
dp = Dispatcher(bot=bot, storage=storage)
user = db.DataBase('exchange_tracker', 'users', credentials['database']['token'], '_id')
scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Kiev"))
