import asyncio
import logging

import sentry_sdk
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN, SENTRY_DSN
from globals import Globals
from routers.settings_router import settings_router
from routers.ban_router import ban_router
from routers.help_router import help_router
from routers.mute_router import mute_router
from routers.registration_router import registration_router
from routers.roleplay_router import roleplay_router
from routers.warn_router import warn_router
from utils import init_db

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0
)

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(help_router)
dp.include_router(mute_router)
dp.include_router(ban_router)
dp.include_router(roleplay_router)
dp.include_router(warn_router)
dp.include_router(registration_router)
dp.include_router(settings_router)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    Globals()
    engine = init_db()
    Globals.db_engine = engine
    dp.run_polling(bot)
