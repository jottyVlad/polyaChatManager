from aiogram import types
from tortoise import Tortoise, Model

from models import ChatMember


async def init_db():
    # Here we create a SQLite DB using file "db.sqlite3"
    #  also specify the app name of "models"
    #  which contain models from "app.models"
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


async def get_chatmember_or_none(chat_id: int,
                                  user_id: int
                                  ) -> ChatMember:
    user = await ChatMember.get_or_none(chat_id=chat_id,
                                        user_id=user_id)
    return user


async def create_chatmember(chat_id: int,
                             user_id: int,
                             warns: int = 0) -> ChatMember:
    user = await ChatMember.create(chat_id=chat_id,
                                   user_id=user_id,
                                   warns=warns)
    return user


async def save_model(model: Model) -> None:
    await model.save()
    return None
