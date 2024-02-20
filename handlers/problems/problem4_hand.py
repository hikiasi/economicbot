"""
Модуль для обработки сообщений и управления состояниями для решения задачи расчета прибыли фирмы.
"""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import reply
from utils.problem4states import Problem4States
from utils.validators import validate_input_int


router = Router()


@router.message(F.text.lower().in_(["4 задача"]))
async def handle_problem4(message: Message, state: FSMContext):
    """
    Обрабатывает команду на начало решения задачи расчета прибыли фирмы.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    await message.answer(
        "Вы выбрали задачу для расчета прибыли фирмы🏅\nПосле того, как Вы"
        " введете все параметры, Вы получите ответ с итоговой прибылью с"
        " учетом всех издержек.\nВведите объем производства (Q):",
        reply_markup=reply.in_task,
    )
    await state.set_state(Problem4States.InputQ)


@router.message(Problem4States.InputQ)
async def input_q(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод объема производства (Q).

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_int(message, state, "Q"):
        await message.answer(
            "Отлично! Теперь введите цену в штуках (P):",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem4States.InputP)


@router.message(Problem4States.InputP)
async def input_p(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод цены в штуках (P).

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_int(message, state, "P"):
        await message.answer(
            "Прекрасно! Теперь введите данные о переменных издержках.\n"
            "Пример ввода: 'Оплата топлива, 5'\n"
            "Для каждого типа издержек введите от 0 до 5 строк.",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem4States.InputVC)


@router.message(Problem4States.InputVC)
async def input_vc(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод данных о переменных издержках.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    try:
        # Разбиваем входное сообщение на строки по символу новой строки
        variables = message.text.split("\n")

        # Инициализируем переменную для хранения общей суммы переменных издержек
        VC_total = 0

        # Создаем пустой список для хранения информации о переменных издержках
        VC_info = []

        # Проверяем, если количество строк больше 5
        if len(variables) > 5:
            # Отправляем сообщение пользователю о том, что будут учтены только первые 5 строк
            await message.answer(
                "Вы ввели больше 5 строк, в решении будут учтены только первые"
                " 5 строк📋",
                reply_markup=reply.in_task,
            )
        for variable in variables[:5]:  # Ограничим ввод до 5 строк
            # Разбиваем строку на части по запятой
            data = variable.split(",")

            # Проверяем, что строка содержит две части (название и стоимость)
            if len(data) == 2:
                # Извлекаем название и стоимость из данных
                name, cost = data

                # Преобразуем стоимость в целое число, удаляем возможные пробелы
                cost = int(cost.strip())
                if cost <= 0:
                    await message.answer(
                        "Издержки не могут быть нулевыми или отрицательными."
                        " Пожалуйста, укажите положительное значение"
                        " издержек.",
                        reply_markup=reply.in_task,
                    )
                    return

                # Увеличиваем общую сумму переменных издержек
                VC_total += cost

                # Добавляем информацию о переменных издержках в список
                VC_info.append((name.strip(), cost))

            # Проверяем, если строка не пустая (если пустая, значит просто Enter)
            elif variable.strip():  # Проверка на пустые строки
                await message.answer(
                    "Неверный формат ввода данных. Пожалуйста, введите данные"
                    " о переменных издержках.\nПример ввода: 'Оплата топлива,"
                    " 5'\n",
                    reply_markup=reply.in_task,
                )
                return

        # Обновляем состояние FSM с общей суммой переменных издержек и информацией о них
        await state.update_data(VC_total=VC_total, VC_info=VC_info)

        # Отправляем сообщение пользователю о необходимости ввода данных о постоянных издержках
        await message.answer(
            "Прекрасно! Теперь введите данные о постоянных издержках.\n"
            "Пример ввода: 'Аренда зала, 200000'\n",
            reply_markup=reply.in_task,
        )

        # Устанавливаем следующее состояние FSM для ввода данных о постоянных издержках
        await state.set_state(Problem4States.InputFC)
    except ValueError:
        await message.answer("Пожалуйста, введите целое число.")


@router.message(Problem4States.InputFC)
async def input_fc(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод данных о постоянных издержках.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    try:
        variables = message.text.split("\n")
        FC_total = 0
        FC_info = []
        if len(variables) > 5:
            await message.answer(
                "Вы ввели больше 5 строк, в решении будут учтены только первые"
                " 5 строк📋",
                reply_markup=reply.in_task,
            )
        for variable in variables[:5]:  # Ограничим ввод до 5 строк
            data = variable.split(",")
            if len(data) == 2:
                name, cost = data
                cost = int(cost.strip())
                if cost <= 0:
                    await message.answer(
                        "Издержки не могут быть нулевыми или отрицательными."
                        " Пожалуйста, укажите положительное значение"
                        " издержек.",
                        reply_markup=reply.in_task,
                    )
                    return
                FC_total += cost
                FC_info.append((name.strip(), cost))
            elif variable.strip():  # Проверка на пустые строки
                await message.answer(
                    "Неверный формат ввода данных. Пожалуйста, введите данные"
                    " о постоянных издержках.\nПример ввода: 'Аренда зала,"
                    " 200000'\n",
                    reply_markup=reply.in_task,
                )
                return

        await state.update_data(FC_total=FC_total, FC_info=FC_info)

        # Получаем все значения из состояния
        data = await state.get_data()

        # Формируем текст ответа
        response = (
            f"При реализации {data['Q']} единиц продукции по {data['P']} руб."
            " за единицу товара и "
            f"уровне переменных издержек в {data['VC_total']} руб./единицу"
            " товара "
            "(включая:"
            f" {', '.join([f'{name} ({cost} руб./ед.)' for name, cost in data['VC_info']])}) "
            f"и постоянных издержек в {data['FC_total']} руб. "
            "(включая:"
            f" {', '.join([f'{name} ({cost} руб.)' for name, cost in data['FC_info']])}), "
            "прибыль составит: "
            f"{data['P'] * data['Q'] - data['FC_total'] - data['VC_total'] * data['Q']} руб."
        )

        # Отправляем ответ пользователю
        await message.answer(response, reply_markup=reply.main)

        # Сбрасываем состояние
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите целое число.")
