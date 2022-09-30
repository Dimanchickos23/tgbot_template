from aiogram import types, Dispatcher, Bot


async def new_member(message: types.Message):
    members = ", ".join([m.get_mention(as_html=True) for m in message.new_chat_members])
    await message.reply(f"Привет, {members}.")


async def banned_member(message: types.Message):
    bot = Bot.get_current()
    if message.left_chat_member.id == message.from_user.id:
        await message.answer(f"{message.left_chat_member.get_mention(as_html=True)} вышел из чата")
    elif message.from_user.id == (await bot.me).id:
        return
    else:
        await message.answer(f"{message.left_chat_member.full_name} был удален из чата"
                             f"пользователем {message.from_user.get_mention(as_html=True)}.")


def register_service_messages(dp: Dispatcher):
    dp.register_message_handler(new_member, content_types=types.ContentType.NEW_CHAT_MEMBERS)
    dp.register_message_handler(banned_member, content_types=types.ContentType.LEFT_CHAT_MEMBER)
