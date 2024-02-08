from aiogram.types import (
    InlineKeyboardButton, InlineKeyboardMarkup
) 

links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Telegram", url="tg://resolve?domain=hikiasi"),
            InlineKeyboardButton(text="Yandex", url="https://ya.ru")
        ]
    ]
)