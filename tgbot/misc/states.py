from aiogram.dispatcher.filters.state import StatesGroup, State


class Survey(StatesGroup):
    FIO = State()
    Age = State()
    Height = State()
    Bust = State()
    Waist = State()
    Hips = State()
    Size = State()
    Leg_size = State()
    Disk = State()


class Prolong(StatesGroup):
    First = State()


class NewPost(StatesGroup):
    EnterMessage = State()
    When = State()
    Confirm = State()
    Final = State()


class DataState(StatesGroup):
    One = State()