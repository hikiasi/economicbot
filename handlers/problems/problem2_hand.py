"""
Модуль для обработки сообщений и управления состояниями для решения задачи по нахождению точки рыночного равновесия.
"""

from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.problem2states import Problem2States
from utils.validators import validate_input_float

from keyboards import reply

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

    await message.answer("Вы выбрали задачу по нахождению точки рыночного равновесия🥈\n"
                         "После того, как Вы введете все параметры, Вы получите значения цены равновесия, объема спроса и объема предложения.\n"
                         "Введите коэффициент A:", reply_markup=reply.in_task)
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

    if await validate_input_float(message, state, 'A'):
        await message.answer("Отлично! Теперь введите коэффициент B:", reply_markup=reply.in_task)
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

    if await validate_input_float(message, state, 'B'):
        await message.answer("Прекрасно! Теперь введите коэффициент C:", reply_markup=reply.in_task)
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

    if await validate_input_float(message, state, 'C'):
        await message.answer("Отлично! Теперь введите коэффициент D:", reply_markup=reply.in_task)
        await state.set_state(Problem2States.InputD)


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

    if await validate_input_float(message, state, 'D'):

        # Получаем все значения из состояния
        data = await state.get_data()

        # Вычисляем равновесие по формулам спроса и предложения
        P = (data['C'] - data['A']) / (data['B'] + data['D'])
        Qd = data['A'] * P - data['B']
        Qs = data['C'] - data['D'] * P

        # Отправляем ответ пользователю
        await message.answer(f"Цена равновесия: {P:.2f}\n"
                             f"Объем спроса: {Qd:.2f}\n"
                             f"Объем предложения: {Qs:.2f}", reply_markup=reply.main)

        # Сбрасываем состояние
        await state.clear()
