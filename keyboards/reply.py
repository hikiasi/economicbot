"""
Модуль, содержащий клавиатуру для пользователя.
"""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# Основная клавиатура для выбора задач
main = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="1 задача"),
            KeyboardButton(text="2 задача"),
        ],
        [
            KeyboardButton(text="3 задача"),
            KeyboardButton(text="4 задача"),
        ],
    ],
    resize_keyboard=True,  # Разрешить изменение размера клавиатуры
    one_time_keyboard=True,
    input_field_placeholder="Выберите задачу из меню",  # Placeholder для поля ввода
    selective=True,
)

# Клавиатура для отмены текущей задачи и возврата к основному меню
in_task = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отмена")]],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите задачу из меню",
    selective=True,
)
