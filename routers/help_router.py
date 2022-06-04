from aiogram import Router, types

help_router = Router()


@help_router.message(commands=["start", "help"])
async def help_handler(message: types.Message):
    await message.reply("Помощь по командам")
