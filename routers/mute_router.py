from aiogram import Router, types, Bot
from aiogram.types import ChatPermissions

from filters.adminperm_filter import UserAdminPermissionRequired, \
    BotAdminPermissionRequired
from filters.chattype_filter import ChatType

mute_router = Router()

mute_router.message.bind_filter(ChatType)
mute_router.message.bind_filter(UserAdminPermissionRequired)
mute_router.message.bind_filter(BotAdminPermissionRequired)


@mute_router.message(commands=['mute'])
async def mute_handler(message: types.Message):
    bot = Bot.get_current()
    admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]

    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека, которого надо замьютить")
        return

    if message.reply_to_message.from_user in admins:
        await message.reply("Нельзя замьютить администратора")
        return

    permissions = ChatPermissions()
    permissions.can_send_messages = False

    await bot.restrict_chat_member(message.chat.id,
                                   message.reply_to_message.from_user.id,
                                   permissions)

    await message.reply("Пользователь замьючен")


@mute_router.message(commands=['unmute'])
async def unmute_handler(message: types.Message):
    bot = Bot.get_current()
    admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]

    if not message.reply_to_message:
        await message.reply("Перешлите сообщение человека, которого надо размьютить")
        return

    if message.reply_to_message.from_user in admins:
        await message.reply("Нельзя размьютить администратора")
        return

    permissions = ChatPermissions()
    permissions.can_send_messages = True

    await bot.restrict_chat_member(message.chat.id,
                                   message.reply_to_message.from_user.id,
                                   permissions)

    await message.reply("Пользователь размьючен")
