from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic, hstrikethrough, hlink, hunderline, hcode


async def user_start(message: Message):
    await message.reply("Hello, user!")


html_text = "\n".join(
    [
        "Привет, " + hbold("Костя!"),
        "Как говорится:",
        hitalic("Бояться надо не смерти, а пустой жизни."),
        "",
        "Но мы сейчас не об этом. " + hstrikethrough("Что тебе нужно?"),
        "Этот текст с HTML форматированием. "
        "Почитать об этом можно " + hlink("тут",
                                          "https://core.telegram.org/bots/api#formatting-options"),
        hunderline("Внимательно прочти и используй с умом!"),
        "",
        hcode("Пример использования - ниже:"),
        "",
        ""]
)
html_text += hcode(html_text)


async def show_parse_mode(message: Message):
    await message.answer(html_text)
    # await message.answer(html_text, parse_mode=types.ParseMode.HTML)


def register_user(dp: Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(show_parse_mode, commands=["parse_mode_html"], state="*")
