import dataclasses
from typing import Optional

from aiogram import Router, types

from filters.chattype_filter import ChatType
from utils import get_chatsettings_or_none, create_chatsettings

roleplay_router = Router()
roleplay_router.message.bind_filter(ChatType)


@dataclasses.dataclass
class RoleplayCommandSettings:
    text: str
    smile: str
    is_nsfw: bool


roleplay_commands: dict[str, RoleplayCommandSettings] = {
    "трахнуть": RoleplayCommandSettings(
        text="трахнул(-а)", smile="🥰", is_nsfw=True
    ),
    "выебать": RoleplayCommandSettings(
        text="жёстко выебал(-а)", smile="😍", is_nsfw=True
    ),
    "обнять": RoleplayCommandSettings(
        text="обнял(-а)", smile="😊", is_nsfw=False
    ),
    "поцеловать": RoleplayCommandSettings(
        text="поцеловал(-а)", smile="😘", is_nsfw=False
    ),
    "въебать": RoleplayCommandSettings(
        text="въебал(-а)", smile="😈", is_nsfw=True),
    "ударить": RoleplayCommandSettings(
        text="ударил(-а)", smile="😈", is_nsfw=False
    )
}


async def process_roleplay_command(message: types.Message, text: str, smile: Optional[str] = None):
    additional = ""
    if len(message.text.split()) > 1:
        additional = " ".join(message.text.split()[1:])

    if message.reply_to_message:
        if additional:
            answer = f"{message.from_user.first_name} " \
                     f"{text} {message.reply_to_message.from_user.first_name} " \
                     f"{additional} {smile}"
        else:
            answer = f"{message.from_user.first_name} " \
                     f"{text} {message.reply_to_message.from_user.first_name} {smile}"

        await message.reply(answer)
        return


@roleplay_router.message(text_startswith=list(roleplay_commands.keys()), text_ignore_case=True)
async def roleplay_handler(message: types.Message):
    try:
        chatsettings = get_chatsettings_or_none(message.chat.id)
        if not chatsettings:
            chatsettings = create_chatsettings(message.chat.id)

        command = roleplay_commands[message.text.split()[0].lower()]

        if command.is_nsfw and not chatsettings.allowed_nsfw:
            await message.answer("NSFW команды отключены!")
            return

        await process_roleplay_command(message,
                                       command.text,
                                       command.smile)
    except KeyError:
        return
