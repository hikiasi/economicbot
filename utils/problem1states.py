"""
Модуль, содержащий класс состояний для первой задачи.
"""

from aiogram.fsm.state import State, StatesGroup


class Problem1States(StatesGroup):
    InputA1 = State()
    InputB1 = State()
    InputA2 = State()
    InputB2 = State()
