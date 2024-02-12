"""
Модуль, содержащий класс состояний для четвертой задачи.
"""

from aiogram.fsm.state import State, StatesGroup


class Problem4States(StatesGroup):
    InputQ = State()
    InputP = State()
    InputVC = State()
    InputFC = State()
