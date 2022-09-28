from aiogram.dispatcher.filters.state import StatesGroup, State


class Survey(StatesGroup):
    Name = State()
    Email = State()
    Phone = State()
