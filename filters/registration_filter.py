from aiogram import types, Bot
from aiogram.dispatcher.filters import BaseFilter

from utils import get_user_or_none


class UserRegistrationRequired(BaseFilter):
    async def __call__(self,
                       message: types.Message
                       ) -> bool:
        user = get_user_or_none(message.from_user.id)
        if not user:
            await message.reply("Для выполнения данной команды требуется регистрация! "
                                "Зарегистрируйтесь в личных сообщениях командой /reg")
            return False
        return True
