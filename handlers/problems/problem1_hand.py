import os
from aiogram import Router, F, types
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.enums import ChatAction
from utils.problem1states import Problem1States
from utils.validators import validate_input_float
from .ppf_plotter import plot_PPF
from keyboards import reply
import time


router = Router()


@router.message(F.text.lower().in_(["1 задача"]))
async def handle_problem1(message: Message, state: FSMContext):
    await message.answer("Вы выбрали задачу по построению общей КПВ🥇\n"
                         "После того, как Вы введете все параметры, Вы получите общий график КПВ для двух производителей товаров А и Б.\n"
                         "Введите максимальный объем производства товара А для производителя 1:", reply_markup=reply.in_task)
    await state.set_state(Problem1States.InputA1)


@router.message(Problem1States.InputA1)
async def input_a1(message: types.Message, state: FSMContext):
    if await validate_input_float(message, state, 'a1'):
        await message.answer("Отлично! Теперь введите максимальный объем производства товара Б для производителя 1:", reply_markup=reply.in_task)
        await state.set_state(Problem1States.InputB1)


@router.message(Problem1States.InputB1)
async def input_b1(message: types.Message, state: FSMContext):
    if await validate_input_float(message, state, 'b1'):
        await message.answer("Прекрасно! Теперь введите максимальный объем производства товара А для производителя 2:", reply_markup=reply.in_task)
        await state.set_state(Problem1States.InputA2)


@router.message(Problem1States.InputA2)
async def input_a2(message: types.Message, state: FSMContext):
    if await validate_input_float(message, state, 'a2'):
        await message.answer("Отлично! Теперь введите максимальный объем производства товара Б для производителя 2:", reply_markup=reply.in_task)
        await state.set_state(Problem1States.InputB2)


@router.message(Problem1States.InputB2)
async def input_b2(message: types.Message, state: FSMContext):
    if await validate_input_float(message, state, 'b2'):
        user_id = message.from_user.id

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
        timestamp = int(time.time())  # получаем текущее время в секундах
        # Строим график и сохраняем его на диск
        plot_PPF(data.get('a1'), data.get('b1'), data.get(
            'a2'), data.get('b2'), user_id, timestamp)

        # Отправляем график пользователю
        await message.answer_photo(FSInputFile(f'handlers/problems/{user_id}_{timestamp}.png'), caption="Вот ваш график📊", reply_markup=reply.main)

        os.remove(f"handlers/problems/{user_id}_{timestamp}.png")

        # Сбрасываем состояние
        await state.clear()
