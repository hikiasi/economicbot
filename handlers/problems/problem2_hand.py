"""
Модуль для обработки сообщений и управления состояниями для решения задачи по нахождению точки рыночного равновесия.
"""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import reply
from utils.problem2states import Problem2States
from utils.validators import validate_input_float


router = Router()


@router.message(F.text.lower().in_(["2 задача"]))
async def handle_problem2(message: Message, state: FSMContext):
    """
    Обрабатывает команду на начало решения задачи по нахождению точки рыночного равновесия.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    await message.answer(
        "Вы выбрали задачу по нахождению точки рыночного равновесия🥈\nПосле"
        " того, как Вы введете все параметры, Вы получите значения цены"
        " равновесия, объема спроса и объема предложения.\nВведите"
        " коэффициент A:",
        reply_markup=reply.in_task,
    )
    await state.set_state(Problem2States.InputA)


@router.message(Problem2States.InputA)
async def input_a(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента A.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_float(message, state, "A"):
        await message.answer(
            "Отлично! Теперь введите коэффициент B:",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem2States.InputB)


@router.message(Problem2States.InputB)
async def input_b(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента B.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_float(message, state, "B"):
        await message.answer(
            "Прекрасно! Теперь введите коэффициент C:",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem2States.InputC)


@router.message(Problem2States.InputC)
async def input_c(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента C.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    # if await validate_input_float(message, state, "C"):
    try:
        C = float(message.text)
        await state.update_data(C=C)

        await message.answer(
            "Отлично! Теперь введите коэффициент D:",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem2States.InputD)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem2States.InputD)
async def input_d(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента D и вычисляет точку рыночного равновесия.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_float(message, state, "D"):

        # Получаем все значения из состояния
        data = await state.get_data()

        # Вычисляем равновесие по формулам спроса и предложения
        P = (
            ((data["C"] - data["A"]) / (data["B"] + data["D"])) * (-1)
            if (data["B"] + data["D"]) != 0
            else 0
        )
        # Заменяем отрицательное значение или отрицательный ноль на ноль
        P = max(0, P)
        Qd = max(0, data["A"] * P - data["B"])

        # Вычисляем объем предложения
        Qs = max(0, data["C"] + data["D"] * P)

        # Решение задачи
        solution = (
            f"Условие равновесия: Qd = Qs, т.е.:\n{data['A']} - {data['B']}P ="
            f" {data['C']}+{data['D']}P\n{data['A']} - {data['C']} ="
            f" {data['D']}P + {data['B']}P\n{data['A'] - data['C']} ="
            f" {data['D'] + data['B']}P\n"
            f"{P} = Pe\nQe = {Qs}\n\nТаким"
            f" образом, равновесная цена Pe = {P}, равновесное предложение Qe"
            f" = {Qs}\nОбъем спроса: {Qd:.2f}"
        )

        # Отправляем ответ пользователю
        await message.answer(
            f"{solution}",
            reply_markup=reply.main,
        )

        # Сбрасываем состояние
        await state.clear()
