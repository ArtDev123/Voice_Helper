from aiogram.fsm.state import StatesGroup, State

class StepsForm(StatesGroup):
    CHOOSE_ACTION = State()
    VOICE = State()