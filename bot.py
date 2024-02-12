"""
Модуль запуска бота и настройки dispatcher.

Содержит функцию:
- main(): основная функция для запуска бота.
"""

import asyncio

from aiogram import Bot, Dispatcher

# Импорт конфигурации бота
from config_reader import config

# Импорт роутеров и коллбэков
from handlers import problems, user_commands


async def main():
    """
    Основная функция для запуска бота.

    Создает экземпляр бота и dispatcher'a, подключаем роутеры и запускаем бота
    """

    # Создаем экземпляр бота с использованием токена из конфигурации
    bot = Bot(config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()

    # Подключаем роутеры для обработки сообщений и коллбэков
    dp.include_routers(
        user_commands.router,
        problems.router,
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
