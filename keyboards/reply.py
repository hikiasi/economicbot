from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.filters import Command

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
        # [
        #     KeyboardButton(text="Отмена задачи", callback_data=Command('cancel'))
        # ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите задачу из меню",
    selective=True
)

in_task = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите задачу из меню",
    selective=True
)
