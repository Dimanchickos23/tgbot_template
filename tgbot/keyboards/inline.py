from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

keyboard = InlineKeyboardMarkup(row_width=2)
keyboard_cb = CallbackData('call', 'action')

edit_name = InlineKeyboardButton(text="Edit Name", callback_data=keyboard_cb.new(action='edit_name'))
edit_descr = InlineKeyboardButton(text="Edit Description", callback_data=keyboard_cb.new(action='edit_descr'))
edit_about = InlineKeyboardButton(text="Edit About", callback_data=keyboard_cb.new(action='edit_about'))
edit_pic = InlineKeyboardButton(text="Edit Botpic", callback_data=keyboard_cb.new(action='edit_pic'))
edit_commands = InlineKeyboardButton(text="Edit Commands", callback_data=keyboard_cb.new(action='edit_commands'))
back_to_bot = InlineKeyboardButton(text="<<Back to Bot", callback_data=keyboard_cb.new(action="back_to_bot"))

keyboard.insert(edit_name)
keyboard.insert(edit_descr)
keyboard.insert(edit_about)
keyboard.insert(edit_pic)
keyboard.insert(edit_commands)
keyboard.insert(back_to_bot)