from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from tgbot.misc import Test


async def enter_test(message: types.Message):
    await message.answer("Вы начали тестирование.\n"
                         "Вопрос №1. \n\n"
                         "Вы часто занимайтесь бессмысленными делами"
                         "(бесцельно лазаете по интернету, клацаете пультом телевизора, просто смотрите в стену )")
    await Test.Q1.set()
    # await Test.first() это тоже самое


async def q1_answer(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(answer1=answer)
    # await state.update_data(
    #     {
    #         "answer1": answer
    #     }
    # )
    # async with state.proxy() as data:
    #     data["answer1"] = answer
    await message.answer("Вопрос №2. \n\n"
                         "Ваша память ухудшилась и вы помните то, что было давно, но забывайте недавние события")

    await Test.Q2.set()


async def q2_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = message.text

    await message.answer("Спасибо за ваши ответы")
    await message.answer(f"Ответ 1: {answer1}")
    await message.answer(f"Ответ 2: {answer2}")

    await state.finish()
    # await state.reset_state(with_data=False) сбрасывает состояние, сохраняя данные


def register_test(dp: Dispatcher):
    dp.register_message_handler(enter_test, Command("test"))
    dp.register_message_handler(q1_answer, state=Test.Q1)
    dp.register_message_handler(q2_answer, state=Test.Q2)