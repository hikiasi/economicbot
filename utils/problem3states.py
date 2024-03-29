"""
Модуль, содержащий класс состояний для третьей задачи.
"""

from aiogram.fsm.state import State, StatesGroup


class Problem3States(StatesGroup):
    InputA = State()
    InputB = State()
    InputC = State()
    InputD = State()
    InputE = State()
