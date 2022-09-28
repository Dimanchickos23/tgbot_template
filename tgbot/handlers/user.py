from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from tgbot_template.tgbot.keyboards.reply import menu


async def user_start(message: Message):
    await message.reply("Hello, user!")


async def show_menu(message: Message):
    await message.answer("Выберите товар в меню ниже", reply_markup=menu)


async def get_cotletki(message: Message):
    await message.answer("Вы выбрали котлетки.")


async def garnir(message: Message):
    await message.answer(f"Вы выбрали {message.text}", reply_markup=ReplyKeyboardRemove())


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(show_menu, Command("menu"))
    dp.register_message_handler(get_cotletki, text="Котлетки")
    dp.register_message_handler(garnir, Text(equals=["Пюрешка", "Макарошки"]))
