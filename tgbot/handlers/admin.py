import datetime

from aiogram import Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler_di import ContextSchedulerDecorator

from tgbot_template.tgbot.keyboards.inline import confirmation_keyboard, post_callback
from tgbot_template.tgbot.misc.states import NewPost, DataState

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


async def create_post(message: Message):
    await message.answer("Отправьте мне текст поста на публикацию")
    await NewPost.EnterMessage.set()


async def enter_message(message: Message, state: FSMContext):
    await state.update_data(text=message.html_text, mention=message.from_user.get_mention())
    await message.answer(f"На сколько часов вы хотите опубликовать пост?\n"
                         f"Введите число.")
    await NewPost.next()


async def when_close_post(message: Message, state: FSMContext):
    await state.update_data(hours=int(message.text))
    await message.answer(f"Вы собираетесь отправить пост на проверку?",
                         reply_markup=confirmation_keyboard)
    await NewPost.next()


async def confirm_post(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        text = data.get("text")
        mention = data.get("mention")
        hours = data.get("hours")
    await NewPost.next()
    await call.message.edit_reply_markup()
    await call.message.answer("Вы отправили пост на проверку")
    await call.message.answer(f"Пользователь {mention} хочет сделать пост длительностью {hours}:")
    await call.message.answer(text, parse_mode="HTML", reply_markup=confirmation_keyboard)


async def cancel_post(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_reply_markup()
    await call.message.answer("Вы отклонили пост")


async def _post_unknown(message: Message):
    await message.answer("Выберите опубликовать или отклонить пост")


async def close_casting(message_id: int, message_text: str, chat_id: int):
    bot = Bot.get_current()
    await bot.edit_message_text(message_text + "\n<b>Закрыто</b>", chat_id, message_id, parse_mode="HTML", reply_markup=None)


async def approve_post(call: CallbackQuery, callback_data: dict,  scheduler: AsyncIOScheduler, state: FSMContext):
    await call.answer("Вы одобрили этот пост.", show_alert=True)

    target_channel = -1001816253590
    message = await call.message.edit_reply_markup()
    user_id = str(call.from_user.id)
    data = await state.get_data()
    hours = data.get("hours")

    casting = InlineKeyboardMarkup(row_width=1)
    confirm = InlineKeyboardButton(text="Откликнуться", url=f"tg://user?id={user_id}", callback_data="custom callback")
    casting.insert(confirm)
    cancel = InlineKeyboardButton(text="Отказаться", callback_data=user_id)
    casting.insert(cancel)

    message = await message.send_copy(chat_id=target_channel, reply_markup=casting)
    mes_id = message.message_id
    text = message.text
    ch_id = message.chat.id
    scheduler.add_job(close_casting, 'date', run_date=datetime.datetime.now()+datetime.timedelta(hours=hours), kwargs=dict(message_id=mes_id, message_text=text, chat_id=ch_id))
    await state.finish()


async def decline_post(call: CallbackQuery):
    await call.answer("Вы отклонили этот пост.", show_alert=True)
    await call.message.edit_reply_markup()


async def reset_state(message: Message, state: FSMContext):
    await state.finish()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], state="*", is_admin=True)
    dp.register_message_handler(reset_state, commands=["reset"], state="*", is_admin=True)
    dp.register_message_handler(create_post, Command("create_post"), is_admin=True)
    dp.register_message_handler(enter_message, state=NewPost.EnterMessage)
    dp.register_message_handler(when_close_post, state=NewPost.When)
    dp.register_callback_query_handler(confirm_post, post_callback.filter(action="post"), state=NewPost.Confirm)
    dp.register_callback_query_handler(cancel_post, post_callback.filter(action="cancel"), state=NewPost.Confirm)
    dp.register_message_handler(_post_unknown, state=NewPost.Confirm)
    dp.register_callback_query_handler(approve_post, post_callback.filter(action="post"), is_admin=True, state=NewPost.Final)
    dp.register_callback_query_handler(decline_post, post_callback.filter(action="cancel"), is_admin=True, state=NewPost.Final)
