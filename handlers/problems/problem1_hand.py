import os
from aiogram import Router, F, types
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from utils.problem1states import Problem1States
from .ppf_plotter import plot_PPF



router = Router()


@router.message(F.text.lower().in_(["1 задача"]))
async def handle_problem1(message: Message, state: FSMContext):
    await message.answer("Давайте начнем решать первую задачу! Введите максимальный объем производства товара А для производителя 1:")
    await state.set_state(Problem1States.InputA1)


@router.message(Problem1States.InputA1)
async def input_a1(message: types.Message, state: FSMContext):
    try:
        input_value = float(message.text)
        await state.update_data(a1=input_value)
        await message.answer(f"Отлично! Теперь введите максимальный объем производства товара Б для производителя 1:")
        await state.set_state(Problem1States.InputB1)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem1States.InputB1)
async def input_b1(message: types.Message, state: FSMContext):
    try:
        input_value = float(message.text)
        await state.update_data(b1=input_value)
        await message.answer(f"Прекрасно! Теперь введите максимальный объем производства товара А для производителя 2:")
        await state.set_state(Problem1States.InputA2)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem1States.InputA2)
async def input_a2(message: types.Message, state: FSMContext):
    try:
        input_value = float(message.text)
        await state.update_data(a2=input_value)
        await message.answer(f"Отлично! Теперь введите максимальный объем производства товара Б для производителя 2:")
        await state.set_state(Problem1States.InputB2)
    except ValueError:
        await message.answer("Пожалуйста, введите число.")


@router.message(Problem1States.InputB2)
async def input_b2(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    input_value = float(message.text)
    await state.update_data(b2=input_value)

    # Получаем все значения из состояния
    data = await state.get_data()

    await message.answer("Все необходимые данные получены! Вот что вы ввели:\n"
                         f"Максимальный объем производства товара А для производителя 1: {data.get('a1')}\n"
                         f"Максимальный объем производства товара Б для производителя 1: {data.get('b1')}\n"
                         f"Максимальный объем производства товара А для производителя 2: {data.get('a2')}\n"
                         f"Максимальный объем производства товара Б для производителя 2: {data.get('b2')}\n"
                         )

    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.UPLOAD_DOCUMENT
    )
    # Строим график и сохраняем его на диск
    plot_PPF(data.get('a1'), data.get('b1'), data.get(
        'a2'), data.get('b2'), user_id)

    # Отправляем график пользователю
    await message.answer_photo(FSInputFile(f'handlers/problems/{user_id}.png'), caption="Вот ваш график📊")

    os.remove(f"handlers/problems/{user_id}.png")

    # Сбрасываем состояние
    await state.clear()
