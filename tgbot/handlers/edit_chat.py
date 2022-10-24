import io

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command

from tgbot.filters.admin import AdminFilter
from tgbot.filters.group_chat import IsGroup


async def set_new_photo(message: types.Message.reply):
    source_message = message.reply_to_message
    photo = source_message.photo[-1]
    photo = await photo.download(destination=io.BytesIO())
    input_file = types.InputFile(photo)
    # Вариант 1
    # await bot.set_chat_photo(message.chat.id, photo=input_file)
    # Вариант 2
    await message.chat.set_photo(photo=input_file)


async def set_new_title(message: types.Message):
    source_message = message.reply_to_message
    title = source_message.text
    # Вариант 1
    # await bot.set_chat_title(message.chat.id, title=title)

    # Вариант 2
    await message.chat.set_title(title=title)


async def set_new_description(message: types.Message):
    source_message = message.reply_to_message
    description = source_message.text

    # Вариант 1
    # await bot.set_chat_description(message.chat.id, description=description)

    # Вариант 2
    await message.chat.set_description(description=description)


def register_edit_chat(dp: Dispatcher):
    dp.register_message_handler(set_new_photo, IsGroup(), Command("set_photo", prefixes="!/"), is_admin=True)
    dp.register_message_handler(set_new_title, IsGroup(), Command("set_title", prefixes="!/"), is_admin=True)
    dp.register_message_handler(set_new_description, IsGroup(), Command("set_description", prefixes="!/"), is_admin=True)
