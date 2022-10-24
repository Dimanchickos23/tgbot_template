from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.keyboards.inline import keyboard


async def user_start(message: Message):
    await message.reply("Hello, user!")


async def inline_buttons_1(message: Message):
    await message.answer("Edit @Sberleadbot info.\n"
                         "Name: Бот для Заданий на Курсе Udemy\n"
                         "Description: ?\n"
                         "About: ?\n"
                         "Botpic: ? no botpic\n"
                         "Commands: no commands yet", reply_markup=keyboard)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(inline_buttons_1, commands=["inline_buttons_1"])