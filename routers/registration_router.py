from aiogram import Router, types

from filters.chattype_filter import PrivateType

from repositories.user_repository import UserRepository

registration_router = Router()

registration_router.message.bind_filter(PrivateType)


@registration_router.message(commands=["reg"])
async def registration_handler(message: types.Message,
                               user_repository: UserRepository):
    user = user_repository.get(user_id=message.from_user.id)
    if not user:
        user_repository.create(user_id=message.from_user.id)
        await message.reply("Пользователь создан!")
    else:
        await message.reply("Пользователь уже существует!")
