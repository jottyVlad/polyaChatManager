from aiogram import Router, types, Bot
from aiogram.types import MessageEntity

from filters.chattype_filter import ChatType

roleplay_router = Router()
roleplay_router.message.bind_filter(ChatType)


async def process_roleplay_command(message: types.Message, text: str):
    if message.reply_to_message:
        print(5)
        await message.reply(f"{message.from_user.first_name} {text} {message.reply_to_message.from_user.first_name}")
        return

    if len(splitted := message.text.split()) > 1:
        await message.reply(f"{message.from_user.first_name} {text} {' '.join(splitted[1:])}")


@roleplay_router.message(text_startswith=["трахнуть"])
async def trahnut_handler(message: types.Message):
    await process_roleplay_command(message, "трахнул")


@roleplay_router.message(text_startswith=["обнять"])
async def hug_handler(message: types.Message):
    await process_roleplay_command(message, "обнял")
