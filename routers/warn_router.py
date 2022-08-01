from aiogram import Router, types, Bot

from filters.adminperm_filter import UserAdminPermissionRequired
from filters.chattype_filter import ChatType
from repositories.chatmember_repository import ChatMemberRepository

warn_router = Router()

warn_router.message.bind_filter(ChatType)
warn_router.message.bind_filter(UserAdminPermissionRequired)


@warn_router.message(commands=["warn"])
async def warn_handler(message: types.Message,
                       chatmember_repository: ChatMemberRepository):
    bot = Bot.get_current()
    is_admin = (await bot.get_chat_member(message.chat.id, (await bot.me()).id)).status == "administrator"
    if not is_admin:
        await message.reply("Если у бота нет прав администратора, "
                            "то, по достижении максимального количества варнов [3/3] "
                            "у пользователя, он не сможет его забанить!")

    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека, которого нужно заварнить")

    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply("Нельзя заварнить себя")
        return
    if message.reply_to_message.from_user.id == (await bot.me()).id:
        await message.reply("Нельзя заварнить меня, я ведь и обидеться могу =(")
        return

    chatmember = chatmember_repository.get(chat_id=message.chat.id,
                                           user_id=message.reply_to_message.from_user.id)

    if not chatmember:
        chatmember_repository.create(chat_id=message.chat.id,
                                           user_id=message.reply_to_message.from_user.id,
                                           warns=1)
        await message.reply(f"Варн [1/3] выдан пользователю "
                            f"{message.reply_to_message.from_user.first_name}")

    elif chatmember.warns >= 2:
        if is_admin:
            await bot.ban_chat_member(message.chat.id,
                                      message.reply_to_message.from_user.id)

            await message.reply("Пользователь был забанен за "
                                "достижение им максимального количества варнов")
            chatmember.warns = 0
        else:
            chatmember.warns += 1
            await message.reply(f"Варн пользователю выдан, их {chatmember.warns}, "
                                "но у бота нет прав администратора, "
                                "чтобы его забанить")
    else:
        chatmember.warns += 1
        await message.reply(f"Варн [{chatmember.warns}/3] выдан пользователю")

        chatmember_repository.save(chatmember)


@warn_router.message(commands=["remwarn"])
async def remwarn_handler(message: types.Message,
                          chatmember_repository: ChatMemberRepository):
    bot = Bot.get_current()
    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека которого нужно заварнить")
        return

    if message.reply_to_message.from_user.id == message.from_user.id:
        await message.reply("Нельзя разварнить себя, хех...")
        return
    if message.reply_to_message.from_user.id == (await bot.me()).id:
        await message.reply("Нельзя разварнить меня, я и так без варнов =)")
        return

    chatmember = chatmember_repository.get(chat_id=message.chat.id,
                                           user_id=message.reply_to_message.from_user.id)

    if not chatmember:
        await message.reply("У пользователя отсутствуют варны!")

    elif chatmember.warns == 0:
        await message.reply("У пользователя отсутствуют варны!")

    else:
        chatmember.warns -= 1
        await message.reply(f"Варн у пользователя снят, "
                            f"теперь их [{chatmember.warns}/3]")

        chatmember_repository.save(chatmember)


@warn_router.message(commands=["warns"])
async def warns_handler(message: types.Message,
                        chatmember_repository: ChatMemberRepository):
    bot = Bot.get_current()
    if not message.reply_to_message \
            or message.reply_to_message.from_user.id == message.from_user.id:
        chatmember = chatmember_repository.get(chat_id=message.chat.id,
                                               user_id=message.from_user.id)

        if not chatmember:
            await message.reply("У пользователя отстутствуют варны!")
            return
        await message.reply(f"У пользователя {message.from_user.first_name} [{chatmember.warns}/3] варнов!")
        return
    elif message.reply_to_message.from_user.id == (await bot.me()).id:
        await message.reply("У меня нет варнов, очевидно")
        return

    chatmember = chatmember_repository.get(chat_id=message.chat.id,
                                           user_id=message.reply_to_message.from_user.id)
    if not chatmember:
        await message.reply("У пользователя отсутствуют варны!")
        return
    await message.reply(f"У пользователя "
                        f"{message.reply_to_message.from_user.first_name} "
                        f"[{chatmember.warns}/3] варнов!")
