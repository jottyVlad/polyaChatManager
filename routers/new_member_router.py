from aiogram import Router, Bot
from aiogram.types import ContentType, Message

from filters.chattype_filter import ChatType
from utils import get_chatsettings_or_none, create_chatsettings

new_member_router = Router()

new_member_router.message.bind_filter(ChatType)


@new_member_router.message(content_type=[ContentType.NEW_CHAT_MEMBERS])
def new_member_handler(message: Message):
    bot_id = (await Bot.get_current().get_me()).id
    for member in message.new_chat_members:
        if bot_id == member.id:
            chatsettings = get_chatsettings_or_none(message.chat.id)
            if not chatsettings:
                create_chatsettings(message.chat.id)
