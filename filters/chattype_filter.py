from aiogram import types
from aiogram.dispatcher.filters import BaseFilter


class ChatType(BaseFilter):
    chat_types: list[str] = ["group", "supergroup"]

    async def __call__(self,
                       message: types.Message
                       ) -> bool:
        if message.chat.type not in self.chat_types:
            await message.reply("Данная команда доступна только в чатах")
            return False

        return True


class PrivateType(BaseFilter):
    private_type: str = "private"

    async def __call__(self,
                       message: types.Message
                       ) -> bool:

        if message.chat.type != self.private_type:
            await message.reply("Данная команда доступна только в личных сообщениях с ботом")
            return False

        return True
