from aiogram.fsm.state import State, StatesGroup


class NewsLetter(StatesGroup):
    text = State()


class CooperationStates(StatesGroup):
    text_requests = State()


class UserState(StatesGroup):
    get_username = State()
    set_admin = State()
    remove_admin = State()


class AddGroupStates(StatesGroup):
    get_name = State()
    get_username = State()


class GetCointNameStates(StatesGroup):
    get_name_coint = State()
    get_name_coint_weekend = State()
