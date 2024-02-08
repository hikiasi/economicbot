from aiogram.fsm.state import StatesGroup, State


class Problem4States(StatesGroup):
    InputQ = State()
    InputP = State()
    InputVC = State()
    InputFC = State()
