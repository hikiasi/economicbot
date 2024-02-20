"""
Модуль для обработки сообщений и управления состояниями для решения задачи расчета
объема дефицита/излишка на рынке.
"""

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards import reply
from utils.problem3states import Problem3States
from utils.validators import validate_input_float


router = Router()


@router.message(F.text.lower().in_(["3 задача"]))
async def handle_problem3(message: Message, state: FSMContext):
    """
    Обрабатывает команду на начало решения задачи расчета объема дефицита/излишка на рынке.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    await message.answer(
        "Вы выбрали задачу для расчет объема заданных функций спроса и"
        " предложения уровня цены🥉\nПосле того, как Вы введете все параметры,"
        " Вы получите ответ с ситуацией на рынке и какой будет размер дефицита"
        " или излишка.\nВведите коэффициент A:",
        reply_markup=reply.in_task,
    )
    await state.set_state(Problem3States.InputA)


@router.message(Problem3States.InputA)
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
        await state.set_state(Problem3States.InputB)


@router.message(Problem3States.InputB)
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
            "Отлично! Теперь введите коэффициент C:",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem3States.InputC)


@router.message(Problem3States.InputC)
async def input_c(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента C.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """
    try:
        C = float(message.text)
        await state.update_data(C=C)

        await message.answer(
            "Отлично! Теперь введите коэффициент D:",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem3States.InputD)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem3States.InputD)
async def input_d(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента D.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_float(message, state, "D"):
        await message.answer(
            "Отлично! Теперь введите коэффициент E:",
            reply_markup=reply.in_task,
        )
        await state.set_state(Problem3States.InputE)


@router.message(Problem3States.InputE)
async def input_e(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод коэффициента E, вычисляет объем дефицита/излишка на рынке и отправляет
    ответ пользователю.

    Args:
        message: Входящее сообщение.
        state: Состояние FSM.

    Returns:
        None
    """

    if await validate_input_float(message, state, "E"):
        E = float(message.text)
        await state.update_data(E=E)

        # Получаем все значения из состояния
        data = await state.get_data()

        # Вычисляем объемы спроса и предложения при уровне цены E
        Qd = data["A"] - data["B"] * E
        Qs = data["C"] + data["D"] * E

        # Вычисляем разницу между спросом и предложением
        surplus_deficit = round(Qs - Qd, 2)

        # Определяем ситуацию на рынке
        situation = (
            "дефицита"
            if surplus_deficit < 0
            else "излишка" if surplus_deficit > 0 else "равновесия"
        )

        # Формируем сообщение в зависимости от ситуации
        if situation == "равновесия":
            response = (
                f"При уровне цены в {E} денежных единиц на рынке будет"
                f" ситуация {situation}."
            )
        else:
            response = (
                f"При уровне цены в {E} денежных единиц на рынке будет"
                f" ситуация {situation}. Размер {situation} составит:"
                f" {abs(surplus_deficit)} единиц товара."
            )

        # Отправляем ответ пользователю
        await message.answer(
            response,
            reply_markup=reply.main,
        )

        # Сбрасываем состояние
        await state.clear()
