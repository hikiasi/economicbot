from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from utils.problem2states import Problem2States

router = Router()


@router.message(F.text.lower().in_(["2 задача"]))
async def handle_problem2(message: Message, state: FSMContext):
    await message.answer("Давайте начнем решать вторую задачу! Введите коэффициент A:")
    await state.set_state(Problem2States.InputA)


@router.message(Problem2States.InputA)
async def input_a(message: types.Message, state: FSMContext):
    try:
        A = float(message.text)
        await state.update_data(A=A)
        await message.answer("Отлично! Теперь введите коэффициент B:")
        await state.set_state(Problem2States.InputB)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem2States.InputB)
async def input_b(message: types.Message, state: FSMContext):
    try:
        B = float(message.text)
        await state.update_data(B=B)
        await message.answer("Прекрасно! Теперь введите коэффициент C:")
        await state.set_state(Problem2States.InputC)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem2States.InputC)
async def input_c(message: types.Message, state: FSMContext):
    try:
        C = float(message.text)
        await state.update_data(C=C)
        await message.answer("Отлично! Теперь введите коэффициент D:")
        await state.set_state(Problem2States.InputD)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem2States.InputD)
async def input_d(message: types.Message, state: FSMContext):
    try:
        D = float(message.text)
        await state.update_data(D=D)

        # Получаем все значения из состояния
        data = await state.get_data()

        # Вычисляем равновесие по формулам спроса и предложения
        P = (data['C'] - data['A']) / (data['B'] + data['D'])
        Qd = data['A'] * P - data['B']
        Qs = data['C'] - data['D'] * P

        # Отправляем ответ пользователю
        await message.answer(f"Цена равновесия: {P}\n"
                             f"Объем спроса: {Qd}\n"
                             f"Объем предложения: {Qs}")

        # Сбрасываем состояние
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите число.")
