import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from globals import Globals
from routers.help_router import help_router
from routers.mute_router import mute_router
from routers.ban_router import ban_router
from routers.roleplay_router import roleplay_router
from routers.warn_router import warn_router
from routers.registration_router import registration_router
from utils import init_db

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(help_router)
dp.include_router(mute_router)
dp.include_router(ban_router)
dp.include_router(roleplay_router)
dp.include_router(warn_router)
dp.include_router(registration_router)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    Globals()
    engine = init_db()
    Globals.db_engine = engine
    dp.run_polling(bot)

