from aiogram import Router, types, Bot

from filters.adminperm_filter import UserAdminPermissionRequired
from filters.chattype_filter import ChatType
from utils import get_chatmember_or_none, create_chatmember, save_model

warn_router = Router()

warn_router.message.bind_filter(ChatType)
warn_router.message.bind_filter(UserAdminPermissionRequired)


@warn_router.message(commands=["warn"])
async def warn_handler(message: types.Message):
    bot = Bot.get_current()
    # admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]
    is_admin = (await bot.get_chat_member(message.chat.id, (await bot.me()).id)).status == "administrator"
    if not is_admin:
        await message.reply("Если у бота нет прав администратора, "
                            "то, по достижении максимального количества варнов [3/3] "
                            "у пользователя, он не сможет его забанить!")

    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека, которого нужно заварнить")

    user = get_chatmember_or_none(chat_id=message.chat.id,
                                  user_id=message.reply_to_message.from_user.id)

    if not user:
        await create_chatmember(chat_id=message.chat.id,
                                user_id=message.reply_to_message.from_user.id,
                                warns=1)
        await message.reply(f"Варн [{user.warns}/3] выдан пользователю "
                            f"{message.reply_to_message.from_user.first_name}")

    elif user.warns >= 2:
        if is_admin:
            await bot.ban_chat_member(message.chat.id,
                                      message.reply_to_message.from_user.id)

            await message.reply("Пользователь был забанен за "
                                "достижение им максимального количества варнов")
            user.warns = 0
        else:
            user.warns += 1
            await message.reply(f"Варн пользователю выдан, их {user.warns}, "
                                "но у бота нет прав администратора, "
                                "чтобы его забанить")
    else:
        user.warns += 1
        await message.reply(f"Варн [{user.warns}/3] выдан пользователю")

        await save_model(user)


@warn_router.message(commands=["remwarn"])
async def remwarn_handler(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека которого нужно заварнить")
        return

    user = get_chatmember_or_none(chat_id=message.chat.id,
                                  user_id=message.reply_to_message.from_user.id)

    if not user:
        await message.reply("У пользователя отсутствуют варны!")

    elif user.warns == 0:
        await message.reply("У пользователя отсутствуют варны!")

    else:
        user.warns -= 1
        await message.reply(f"Варн у пользователя снят, "
                            f"теперь их [{user.warns}/3]")

        await save_model(user)
