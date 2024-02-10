async def validate_input_float(message, state, state_name):
    try:
        if message.text is None:
            raise ValueError("No value input")

        input_value = float(message.text)

        if input_value <= 0:
            raise ValueError("Not positive")

        if state is not None and await state.get_state() == state_name:
            await state.update_data(**{state_name: input_value})
        return True
    except ValueError as e:
        error_messages = {
            "No value input": "Пожалуйста, введите число.",
            "Not positive": "Пожалуйста, введите положительное вещественное число."
        }
        if state is None or await state.get_state() != state_name:
            error_messages["No value input"] = ""
        await message.answer(error_messages.get(str(e), "Что-то пошло не так, пожалуйста введите вещественное число через точку."))
        return False


async def validate_input_int(message, state, state_name):
    try:
        if message.text is None:
            raise ValueError("No value input")

        input_value = int(message.text)

        if input_value <= 0:
            raise ValueError("Not positive")

        await state.update_data(**{state_name: input_value})
        return True
    except ValueError as e:
        error_messages = {
            "No value input": "Пожалуйста, введите целое число.",
            "Not positive": "Пожалуйста, введите положительное целое число."
        }
        await message.answer(error_messages.get(str(e), "Что-то пошло не так, пожалуйста введите указанное значение."))
        return False