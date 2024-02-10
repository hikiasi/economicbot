from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.problem3states import Problem3States
from utils.validators import validate_input_float

from keyboards import reply

router = Router()


@router.message(F.text.lower().in_(["3 задача"]))
async def handle_problem3(message: Message, state: FSMContext):
    await message.answer("Вы выбрали задачу для расчет объема заданных функций спроса и предложения уровня цены🥉\n"
                         "После того, как Вы введете все параметры, Вы получите ответ с ситуацией на рынке и какой будет размер дефицита или излишка.\n"
                         "Введите коэффициент A:")
    await state.set_state(Problem3States.InputA)


@router.message(Problem3States.InputA)
async def input_a(message: types.Message, state: FSMContext):
    # if await validate_input_float(message, state, 'A'):
    try:
        A = float(message.text)
        await state.update_data(A=A)
        await message.answer("Отлично! Теперь введите коэффициент B:")
        await state.set_state(Problem3States.InputB)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem3States.InputB)
async def input_b(message: types.Message, state: FSMContext):
    # if await validate_input_float(message, state, 'B'):
    try:
        B = float(message.text)
        await state.update_data(B=B)
        await message.answer("Отлично! Теперь введите коэффициент C:")
        await state.set_state(Problem3States.InputC)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem3States.InputC)
async def input_c(message: types.Message, state: FSMContext):
    # if await validate_input_float(message, state, 'C'):
    try:
        C = float(message.text)
        await state.update_data(C=C)
        await message.answer("Отлично! Теперь введите коэффициент D:")
        await state.set_state(Problem3States.InputD)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem3States.InputD)
async def input_d(message: types.Message, state: FSMContext):
    # if await validate_input_float(message, state, 'D'):
    try:
        D = float(message.text)
        await state.update_data(D=D)
        await message.answer("Отлично! Теперь введите коэффициент E:")
        await state.set_state(Problem3States.InputE)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem3States.InputE)
async def input_d(message: types.Message, state: FSMContext):
    try:
        E = float(message.text)
        await state.update_data(E=E)

        # Получаем все значения из состояния
        data = await state.get_data()

        # Вычисляем цену равновесия
        P = (data['C'] - data['A']) / (data['B'] + data['D'])

        # Вычисляем объем спроса и предложения при данной цене
        Qd = data['A'] * P - data['B']
        Qs = data['C'] - data['D'] * P

        # Вычисляем разницу между спросом и предложением
        surplus_deficit = round(Qs - Qd, 2)

        # Определяем ситуацию на рынке
        situation = "дефицит" if surplus_deficit < 0 else "излишек" if surplus_deficit > 0 else "равновесие"

        # Отправляем ответ пользователю
        await message.answer(f"При уровне цены в {E} денежных единиц на рынке будет ситуация {situation}. "
                             f"Размер {situation} составит: {abs(surplus_deficit)} единиц товара.", reply_markup=reply.main)

        # Сбрасываем состояние
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
