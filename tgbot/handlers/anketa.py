from aiogram import Dispatcher, Bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Regexp
from aiogram.types import CallbackQuery

from tgbot_template.tgbot.keyboards.inline import end_survey, url
from tgbot_template.tgbot.misc import Survey
from tgbot_template.tgbot.misc.states import Prolong


async def name_answer(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    # await state.update_data(
    #     {
    #         "answer1": answer
    #     }
    # )
    # async with state.proxy() as data:
    #     data["answer1"] = answer
    await message.answer("Введите ваш возраст:")
    await Survey.Age.set()


async def age_answer(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Введите ваш рост в см:")
    await Survey.Height.set()


async def height_answer(message: types.Message, state: FSMContext):
    await state.update_data(height=message.text)
    await message.answer("Обхват груди в см:")
    await Survey.Bust.set()


async def bust_answer(message: types.Message, state: FSMContext):
    await state.update_data(bust=message.text)
    await message.answer("Обхват талии в см:")
    await Survey.Waist.set()


async def waist_answer(message: types.Message, state: FSMContext):
    await state.update_data(waist=message.text)
    await message.answer("Обхват бедер в см:")
    await Survey.Hips.set()


async def hips_answer(message: types.Message, state: FSMContext):
    await state.update_data(hips=message.text)
    await message.answer("Введите ваш размер одежды (русский):")
    await Survey.Size.set()


async def size_answer(message: types.Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer("Введите ваш размер ноги:")
    await Survey.Leg_size.set()


async def leg_answer(message: types.Message, state: FSMContext):
    await state.update_data(leg=message.text)
    await message.answer("Ссылка на ваше портфолио на Яндекс диске‼️")
    await Survey.Disk.set()


async def disk_answer(message: types.Message, state: FSMContext):
    await state.update_data(disk=message.text)
    data = await state.get_data()
    name = data.get("name")
    age = data.get("age")
    height = data.get("height")
    bust = data.get("bust")
    waist = data.get("waist")
    hips = data.get("hips")
    size = data.get("size")
    leg = data.get("leg")
    disk = data.get("disk")
    beginning = f"{message.from_user.full_name}, проверьте введенные вами данные: \n\n"
    anketa = f"ФИО - {name} \n\nВозраст - {age} \n\nРост - {height} \n\nОбхват груди - {bust} \n\nОбхват талии - {waist} \n\nОбхват бедер - {hips} \n\nРазмер одежды - {size} \n\nРазмер ноги - {leg} \n\nСсылка на портфолио - {disk}"
    ending = "\n\n Если все верно, отправьте данные, нажав на клавишу ⬇️"
    await state.update_data(anketa=anketa)
    await message.answer(beginning + anketa + ending, disable_web_page_preview=True, reply_markup=end_survey)


async def ended_survey(cb: CallbackQuery, state: FSMContext):
    bot = Bot.get_current()
    data = await state.get_data()
    anketa = data.get("anketa")
    await bot.send_message(331572613, anketa, disable_web_page_preview=True)  # chat_id, string
    await cb.message.answer("Также, если у вас нет видео-визитки и снэпов желательно записаться на это занятие,"
                            " так как на большинство кастингов требуются эти материалы ⬇️.", reply_markup=url)
    await cb.message.answer("После оплаты вышлите чек @nzsz13")
    await state.finish()
    await Prolong.First.set()
    await cb.message.answer("Если есть часы на абонементе-позвоните куратору.")
    # await state.finish()

    # ⬇️ await state.reset_state(with_data=False) сбрасывает состояние, сохраняя данные


def register_test(dp: Dispatcher):
    dp.register_message_handler(name_answer, content_types=types.ContentType.TEXT, state=Survey.FIO)
    dp.register_message_handler(age_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Age)
    dp.register_message_handler(height_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Height)
    dp.register_message_handler(bust_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Bust)
    dp.register_message_handler(waist_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Waist)
    dp.register_message_handler(hips_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Hips)
    dp.register_message_handler(size_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Size)
    dp.register_message_handler(leg_answer, Regexp(r'^[0-9]{1,15}$'), state=Survey.Leg_size)
    dp.register_message_handler(disk_answer, Regexp(r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{'
                                                    r'1,6}\b([-a-zA-Z0-9()!@:%_\+.~#?&\/\/=]*)'), state=Survey.Disk)
    dp.register_callback_query_handler(ended_survey, lambda callback_query: callback_query.data == "survey_end",
                                       state=Survey.Disk)
