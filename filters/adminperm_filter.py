from aiogram import types, Bot
from aiogram.dispatcher.filters import BaseFilter


class UserAdminPermissionRequired(BaseFilter):
    async def __call__(self,
                       message: types.Message
                       ) -> bool:
        bot = Bot.get_current()
        admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]
        if message.from_user not in admins:
            await message.reply("Данная команда доступна только администраторам")
            return False

        return True


class BotAdminPermissionRequired(BaseFilter):
    async def __call__(self,
                       message: types.Message
                       ) -> bool:
        bot = Bot.get_current()
        is_admin = (await bot.get_chat_member(message.chat.id, (await bot.me()).id)).status == "administrator"
        if not is_admin:
            await message.reply("Для выполнения данной команды бот должен обладать правами администратора")
            return False

        return True
