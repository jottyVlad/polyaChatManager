import dataclasses

from aiogram import Router, types, Bot

from filters.chattype_filter import ChatType
from repositories.chatsettings_repository import ChatSettingsRepository

settings_router = Router()

settings_router.message.bind_filter(ChatType)


@dataclasses.dataclass
class Parameter:
    list_id: int
    db_name: str
    text: str


parameters = [
    Parameter(list_id=1,
              db_name="roleplay_enabled",
              text="РП команды"),
    Parameter(list_id=2,
              db_name="nsfw_enabled",
              text="18+ РП команды"),
]

bool_text = {
    False: "выключено",
    True: "включено",
}


@settings_router.message(commands=["settings"])
async def settings_handler(message: types.Message,
                           chatsettings_repository: ChatSettingsRepository):
    message_splitted = message.text.split()
    chatsettings = chatsettings_repository.get(chat_id=message.chat.id)

    answer = ""
    if len(message_splitted) == 1:
        for param in parameters:
            answer += f"[{param.list_id}] {param.text}: " \
                      f"{bool_text[chatsettings[param.db_name]]}\n"

        await message.answer(answer)

    # если параметра 2 - просмотр данного параметра
    elif len(message_splitted) == 2:
        try:
            list_id = int(message_splitted[1])
        except ValueError:
            await message.answer("Номер параметра только число!")
            return

        param = list(filter(lambda elem: elem.list_id == list_id,
                            parameters))
        if not param:
            await message.answer("Параметра с таким номером нет!")

        param = param[0]
        await message.answer(f"[{param.list_id}] {param.text}: "
                             f"{bool_text[chatsettings[param.db_name]]}")

    # если параметра 3 - изменение текущего статуса
    elif len(message_splitted) == 3:
        bot = Bot.get_current()
        admins = [i.user for i in await bot.get_chat_administrators(message.chat.id)]

        if message.from_user not in admins:
            await message.answer("Менять настройки могут только администраторы!")
            return
        try:
            list_id = int(message_splitted[1])
            new_status = int(message_splitted[2])
        except ValueError:
            await message.answer("Номер параметра и статус только числа!")
            return

        if new_status not in [0, 1]:
            await message.answer("Cтатус только 0 или 1!")
            return

        new_status = bool(new_status)

        param = list(filter(lambda elem: elem.list_id == list_id,
                            parameters))

        if not param:
            await message.answer("Параметра с таким номером нет!")
            return

        param = param[0]

        chatsettings[param.db_name] = new_status
        chatsettings_repository.save(chatsettings)
        await message.answer("Изменено!")
