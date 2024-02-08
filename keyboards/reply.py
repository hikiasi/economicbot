from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    KeyboardButtonPollType,
    ReplyKeyboardRemove
)

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
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выберите задачу из меню",
    selective=True
)

problem1_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Далее"),
        ],
        [
            KeyboardButton(text="НАЗАД"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

spec = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отправить гео", request_location=True),
            KeyboardButton(text="Отправить гео", request_contact=True),
            KeyboardButton(text="Отправить гео",
                           request_poll=KeyboardButtonPollType(type="quiz")),

        ],
        [
            KeyboardButton(text="НАЗАД")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

rmk = ReplyKeyboardRemove()
