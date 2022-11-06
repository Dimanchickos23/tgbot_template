import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

from tgbot.misc.callback_datas import buy_callback
from tgbot.keyboards.inline import choice, pear_keyboard, apples_keyboard


async def show_items(message: Message):
    await message.answer(text="На продажу у нас есть 2 товара: 5 Яблок и 1 Груша. \n"
                              "Если вам ничего не нужно - жмите отмену",
                         reply_markup=choice)


# Попробуйем отловить по встроенному фильтру, где в нашем call.data содержится "pear"
async def buying_pear(call: CallbackQuery):
    # Обязательно сразу сделать answer, чтобы убрать "часики" после нажатия на кнопку.
    # Укажем cache_time, чтобы бот не получал какое-то время апдейты, тогда нижний код не будет выполняться.
    await call.answer(cache_time=60)

    callback_data = call.data

    # Отобразим что у нас лежит в callback_data
    # logging.info(f"callback_data='{callback_data}'")
    # В питоне 3.8 можно так
    logging.info(f"{callback_data=}")

    await call.message.answer("Вы выбрали купить грушу. Груша всего одна. Спасибо.",
                              reply_markup=pear_keyboard)


# Попробуем использовать фильтр от CallbackData
async def buying_apples(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=60)

    # Выведем callback_data и тут, чтобы сравнить с предыдущим вариантом.
    logging.info(f"{callback_data=}")

    quantity = callback_data.get("quantity")
    await call.message.answer(f"Вы выбрали купить яблоки. Яблок всего {quantity}. Спасибо.",
                              reply_markup=apples_keyboard)


async def cancel_buying(call: CallbackQuery):
    # Ответим в окошке с уведомлением!
    await call.answer("Вы отменили эту покупку!", show_alert=True)

    # Вариант 1 - Отправляем пустую клваиатуру изменяя сообщение, для того, чтобы ее убрать из сообщения!
    await call.message.edit_reply_markup(reply_markup=None)

    # Вариант 2 отправки клавиатуры (по API)
    # await bot.edit_message_reply_markup(chat_id=call.from_user.id,
    #                                     message_id=call.message.message_id,
    #                                     reply_markup=None)


def register_purchase(dp: Dispatcher):
    dp.register_message_handler(show_items, Command("items"))
    dp.register_callback_query_handler(buying_pear, text_contains="pear")
    dp.register_callback_query_handler(buying_apples, buy_callback.filter(item_name="apple"))
    dp.register_callback_query_handler(cancel_buying, text="cancel")
