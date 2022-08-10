from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from repositories.chatsettings_repository import ChatSettingsRepository


class MessageMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        chatsettings_repository: ChatSettingsRepository = data["chatsettings_repository"]

        try:
            chatsettings_repository.get(chat_id=event.chat.id)
        except ValueError:
            chatsettings_repository.create(chat_id=event.chat.id)
        return await handler(event, data)
