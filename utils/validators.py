"""
Модуль, содержащий функции для валидации входных данных.

Содержит функции:
- validate_input_float: для проверки ввода вещественных чисел.
- validate_input_int: для проверки ввода целых чисел.
"""


async def validate_input_float(message, state, state_name):

    """
    Функция для проверки ввода вещественных чисел.

    Args:
        message: Объект сообщения.
        state: Объект состояния FSMContext.
        state_name: Имя состояния для обновления данных.

    Returns:
        bool: Результат проверки (True - ввод верный, False - ввод неверный).
    """

    try:
        if message.text is None:
            # Если значение не введено, вызываем исключение
            raise ValueError("No value input")

        # Преобразуем введенное значение во float
        input_value = float(message.text)

        if input_value <= 0:
            # Если значение не положительное, вызываем исключение
            raise ValueError("Not positive")

        # Обновляем данные состояния
        await state.update_data(**{state_name: input_value})
        return True  # Возвращаем True, если валидация успешна
    except ValueError as e:
        error_messages = {
            "No value input": "Пожалуйста, введите вещественное число через точку.",
            "Not positive": "Пожалуйста, введите положительное вещественное число через точку."
        }
        await message.answer(error_messages.get(str(e), "Что-то пошло не так, пожалуйста введите указанное значение."))
        return False  # Возвращаем False, если валидация не удалась


async def validate_input_int(message, state, state_name):

    """
    Функция для проверки ввода целых чисел.

    Args:
        message: Объект сообщения.
        state: Объект состояния FSMContext.
        state_name: Имя состояния для обновления данных.

    Returns:
        bool: Результат проверки (True - ввод верный, False - ввод неверный).
    """

    try:
        if message.text is None:
            # Если значение не введено, вызываем исключение
            raise ValueError("No value input")

        input_value = int(message.text)  # Преобразуем введенное значение в int

        if input_value <= 0:
            # Если значение не положительное, вызываем исключение
            raise ValueError("Not positive")

        # Обновляем данные состояния
        await state.update_data(**{state_name: input_value})
        return True  # Возвращаем True, если валидация успешна
    except ValueError as e:
        error_messages = {
            "No value input": "Пожалуйста, введите целое число.",
            "Not positive": "Пожалуйста, введите положительное целое число."
        }
        await message.answer(error_messages.get(str(e), "Что-то пошло не так, пожалуйста введите указанное значение."))
        return False  # Возвращаем False, если валидация не удалась
