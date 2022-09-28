from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp

from tgbot_template.tgbot.misc import Survey


async def enter_test(message: types.Message):
    await message.answer("Введите имя:")
    await Survey.Name.set()
    # await Test.first() это тоже самое


async def name_answer(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    # await state.update_data(
    #     {
    #         "answer1": answer
    #     }
    # )
    # async with state.proxy() as data:
    #     data["answer1"] = answer
    await message.answer("Введите Email:")
    await Survey.Email.set()


async def email_answer(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите Номер телефона:")
    await Survey.Phone.set()


async def phone_answer(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    data = await state.get_data()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")

    await message.answer("Привет! Ты ввел следующие данные: \n\n"
                         f"Имя - {name} \n\n"
                         f"Email - {email} \n\n"
                         f"Телефон: - {phone}")

    await state.finish()
    # await state.reset_state(with_data=False) сбрасывает состояние, сохраняя данные


def register_test(dp: Dispatcher):
    dp.register_message_handler(enter_test, Command("form"))
    dp.register_message_handler(name_answer, content_types='text', state=Survey.Name)
    dp.register_message_handler(email_answer, Regexp(r'[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+'), state=Survey.Email)
    dp.register_message_handler(phone_answer, Regexp(r'^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$'),
                                state=Survey.Phone)
