"""
Модуль, содержащий класс состояний для второй задачи.
"""

from aiogram.fsm.state import StatesGroup, State


class Problem2States(StatesGroup):
    InputA = State()
    InputB = State()
    InputC = State()
    InputD = State()
