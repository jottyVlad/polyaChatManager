from aiogram import Router, types, Bot

from filters.adminperm_filter import UserAdminPermissionRequired, \
    BotAdminPermissionRequired
from filters.chattype_filter import ChatType

ban_router = Router()

ban_router.message.bind_filter(ChatType)
ban_router.message.bind_filter(UserAdminPermissionRequired)
ban_router.message.bind_filter(BotAdminPermissionRequired)


@ban_router.message(commands=["ban"])
async def ban_handler(message: types.Message):
    bot = Bot.get_current()
    admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]

    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека, которого надо забанить")
        return

    if message.reply_to_message.from_user in admins:
        await message.reply("Нельзя забанить администратора")
        return

    await bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply("Пользователь забанен")


@ban_router.message(commands=["unban"])
async def unban_handler(message: types.Message):
    bot = Bot.get_current()
    admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]

    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека, которого надо разбанить")
        return

    if message.reply_to_message.from_user in admins:
        await message.reply("Нельзя разбанить администратора")
        return

    await bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    await message.reply("Пользователь разбанен")
