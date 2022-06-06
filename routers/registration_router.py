from aiogram import Router, types

from filters.chattype_filter import PrivateType
from utils import get_user_or_none, create_user

registration_router = Router()

registration_router.message.bind_filter(PrivateType)


@registration_router.message(commands=["reg"])
async def registration_handler(message: types.Message):
    user = get_user_or_none(message.from_user.id)
    if not user:
        create_user(message.from_user.id)
        await message.reply("Пользователь создан!")
    else:
        await message.reply("Пользователь уже существует!")
