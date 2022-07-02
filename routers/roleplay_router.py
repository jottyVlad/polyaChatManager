from typing import Optional

from aiogram import Router, types

from filters.chattype_filter import ChatType

roleplay_router = Router()
roleplay_router.message.bind_filter(ChatType)


async def process_roleplay_command(message: types.Message, text: str, smile: Optional[str] = None):
    if message.reply_to_message:
        await message.reply(f"{message.from_user.first_name} "
                            f"{text} {message.reply_to_message.from_user.first_name} {smile}")
        return

    if len(splitted := message.text.split()) > 1:
        await message.reply(f"{message.from_user.first_name} "
                            f"{text} {' '.join(splitted[1:])} {smile}")


@roleplay_router.message(text_startswith=["трахнуть"], text_ignore_case=True)
async def trahnut_handler(message: types.Message):
    await process_roleplay_command(message, "трахнул(-а)", "🥰")


@roleplay_router.message(text_startswith=["обнять"], text_ignore_case=True)
async def hug_handler(message: types.Message):
    await process_roleplay_command(message, "обнял(-а)", "😊")


@roleplay_router.message(text_startswith=["поцеловать"], text_ignore_case=True)
async def kiss_handler(message: types.Message):
    await process_roleplay_command(message, "поцеловал(-а)", "😘")
