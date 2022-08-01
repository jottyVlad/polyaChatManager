import logging

import sentry_sdk
from aiogram import Bot, Dispatcher
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import BOT_TOKEN, SENTRY_DSN
from models import Base
from repositories.chatmember_repository import ChatMemberRepository
from repositories.user_repository import UserRepository
from routers.ban_router import ban_router
from routers.help_router import help_router
from routers.mute_router import mute_router
from routers.registration_router import registration_router
from routers.roleplay_router import roleplay_router
from routers.warn_router import warn_router

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

if __name__ == '__main__':
    engine = create_engine('sqlite:///bot.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    user_repository = UserRepository(session)
    chatmember_repository = ChatMemberRepository(session)

    dp.run_polling(bot,
                   user_repository=user_repository,
                   chatmember_repository=chatmember_repository)
    session.close()
