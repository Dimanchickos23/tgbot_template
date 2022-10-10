from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from tgbot_template.tgbot.keyboards.inline import prolong_keyboard
from tgbot_template.tgbot.misc.states import Prolong


async def prolong_handler(message: types.Message, state: FSMContext):
    await message.answer("Второй текст отправляется за 1 день до истечения 3-х месячного срока:\n"
                         "Добрый день!\n"
                         "У нас скоро заканчивается контракт с Вами, скажите, пожалуйста, Вам было бы интересно "
                         "продление?\n"
                         "Чтобы больше замотивировать наших моделей на работу, доступ в чат теперь будет платным, "
                         "5000 рублей за 3 месяца.\n"
                         "Мы же со своей стороны постараемся Вас развивать и активно показывать клиентам, если Вам "
                         "интересно реализоваться в этой сфере.", reply_markup=prolong_keyboard)
    await message.answer("По всем вопросам можете писать @lkrioni")
    await state.finish()


def register_prolong(dp: Dispatcher):
    dp.register_message_handler(prolong_handler, state=Prolong.First)
