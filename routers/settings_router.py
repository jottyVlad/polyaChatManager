import dataclasses

from aiogram import Router, Bot
from aiogram.types import Message

from exceptions import ParameterWithDBNameNotFound, ParameterWithIDNotFound
from models import ChatSettings
from utils import get_chatsettings_or_none, create_chatsettings, save_model

settings_router = Router()


@dataclasses.dataclass
class Parameter:
    id: int
    database_name: str
    text: str


parameters = [
    Parameter(id=1,
              database_name="allowed_nsfw",
              text="NSFW команды"),
]

str_bool = {
    True: "true",
    False: "false",
    "true": True,
    "false": False
}


def get_param_status_by_dbname(
        db_name: str,
        chatsettings: ChatSettings
) -> bool:
    if db_name in chatsettings.dict():
        return chatsettings.dict()[db_name]
    raise ParameterWithDBNameNotFound(f"This parameter "
                                      f"with database name: {db_name} "
                                      f"is not found!")


def get_param_by_id(id_: int) -> Parameter:
    for param in parameters:
        if param.id == id_:
            return param
    raise ParameterWithIDNotFound(f"This parameter "
                                  f"with id {id_} "
                                  f"is not found")


def change_status(parameter_textid: str,
                  new_status: bool,
                  chatsettings: ChatSettings) -> ChatSettings | None:

    if parameter_textid == "allowed_nsfw":
        chatsettings.allowed_nsfw = new_status
    return chatsettings


@settings_router.message(commands=["settings"])
async def settings_handler(message: Message):
    chatsettings = get_chatsettings_or_none(message.chat.id)
    if not chatsettings:
        chatsettings = create_chatsettings(message.chat.id)

    if len(message.text.split()) == 1:
        answer_text = ""
        for param in parameters:
            try:
                status = get_param_status_by_dbname(
                    param.database_name,
                    chatsettings
                )
            except AttributeError:
                continue
            answer_text += f"[{param.id}] {param.text}: {status}"

        if answer_text:
            await message.answer(answer_text)
        else:
            await message.answer("Параметры не найдены!")
        return
    else:
        params = message.text.split()[1:]
        if len(params) == 1:
            try:
                param_id = int(params[0])
                parameter = get_param_by_id(param_id)
                text = parameter.text
                status = get_param_status_by_dbname(
                    parameter.database_name, chatsettings
                )
                await message.answer(f"[{param_id}] {text}: {status}")
                return

            except ValueError:
                await message.answer("Параметр может быть только числом!")
            except (ParameterWithDBNameNotFound,
                    ParameterWithIDNotFound):
                await message.answer("Параметр не найден :(")

        elif len(params) == 2:
            bot = Bot.get_current()
            admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]
            if message.from_user not in admins:
                await message.reply("Данная команда доступна только администраторам")
                return
            try:
                param_id = int(params[0])
                parameter = get_param_by_id(param_id)

                new_status = str_bool[params[1].lower()]

                chatsettings = change_status(parameter.database_name,
                                             new_status,
                                             chatsettings)
                if chatsettings:
                    save_model(chatsettings)
                    await message.answer("Изменено!")
                else:
                    await message.answer("Ошибка при обработке команды!")
            except KeyError:
                await message.answer("Статус только true или false!")
