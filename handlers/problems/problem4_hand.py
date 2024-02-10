from aiogram import Router, F, types
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.problem4states import Problem4States
from utils.validators import validate_input_int

from keyboards import reply

router = Router()


@router.message(F.text.lower().in_(["4 задача"]))
async def handle_problem4(message: Message, state: FSMContext):
    await message.answer("Вы выбрали задачу для расчета прибыли фирмы🏅\n"
                         "После того, как Вы введете все параметры, Вы получите ответ с итоговой прибылью с учетом всех издержек.\n"
                         "Введите объем производства (Q):", reply_markup=reply.in_task)
    await state.set_state(Problem4States.InputQ)


@router.message(Problem4States.InputQ)
async def input_q(message: types.Message, state: FSMContext):
    if await validate_input_int(message, state, 'Q'):
        await message.answer("Отлично! Теперь введите цену в штуках (P):", reply_markup=reply.in_task)
        await state.set_state(Problem4States.InputP)


@router.message(Problem4States.InputP)
async def input_p(message: types.Message, state: FSMContext):
    if await validate_input_int(message, state, 'P'):
        await message.answer(
            "Прекрасно! Теперь введите данные о переменных издержках.\n"
            "Пример ввода: 'Оплата топлива, 5'\n"
            "Для каждого типа издержек введите от 0 до 5 строк.", reply_markup=reply.in_task)
        await state.set_state(Problem4States.InputVC)


@router.message(Problem4States.InputVC)
async def input_vc(message: types.Message, state: FSMContext):
    try:
        variables = message.text.split('\n')
        VC_total = 0
        VC_info = []
        if len(variables) > 5:
            await message.answer("Вы ввели больше 5 строк, в решении будут учтены только первые 5 строк📋", reply_markup=reply.in_task)
        for variable in variables[:5]:  # Ограничим ввод до 5 строк
            data = variable.split(',')
            if len(data) == 2:
                name, cost = data
                cost = int(cost.strip())
                if cost <= 0:
                    await message.answer(
                        "Издержки не могут быть нулевыми или отрицательными. Пожалуйста, укажите положительное значение издержек.", reply_markup=reply.in_task)
                    return
                VC_total += cost
                VC_info.append((name.strip(), cost))
            elif variable.strip():  # Проверка на пустые строки
                await message.answer(
                    "Неверный формат ввода данных. Пожалуйста, введите данные о переменных издержках.\n"
                    "Пример ввода: 'Оплата топлива, 5'\n", reply_markup=reply.in_task)
                return

        await state.update_data(VC_total=VC_total, VC_info=VC_info)
        await message.answer(
            "Прекрасно! Теперь введите данные о постоянных издержках.\n"
            "Пример ввода: 'Аренда зала, 200000'\n", reply_markup=reply.in_task)
        await state.set_state(Problem4States.InputFC)
    except ValueError:
        await message.answer("Пожалуйста, введите целое число.")


@router.message(Problem4States.InputFC)
async def input_fc(message: types.Message, state: FSMContext):
    try:
        variables = message.text.split('\n')
        FC_total = 0
        FC_info = []
        if len(variables) > 5:
            await message.answer("Вы ввели больше 5 строк, в решении будут учтены только первые 5 строк📋", reply_markup=reply.in_task)
        for variable in variables[:5]:  # Ограничим ввод до 5 строк
            data = variable.split(',')
            if len(data) == 2:
                name, cost = data
                cost = int(cost.strip())
                if cost <= 0:
                    await message.answer(
                        "Издержки не могут быть нулевыми или отрицательными. Пожалуйста, укажите положительное значение издержек.", reply_markup=reply.in_task)
                    return
                FC_total += cost
                FC_info.append((name.strip(), cost))
            elif variable.strip():  # Проверка на пустые строки
                await message.answer(
                    "Неверный формат ввода данных. Пожалуйста, введите данные о постоянных издержках.\n"
                    "Пример ввода: 'Аренда зала, 200000'\n", reply_markup=reply.in_task)
                return

        await state.update_data(FC_total=FC_total, FC_info=FC_info)

        # Получаем все значения из состояния
        data = await state.get_data()

        # Формируем текст ответа
        response = (
            f"При реализации {data['Q']} единиц продукции по {data['P']} руб. за единицу товара и "
            f"уровне переменных издержек в {data['VC_total']} руб./единицу товара "
            f"(включая: {', '.join([f'{name} ({cost} руб./ед.)' for name, cost in data['VC_info']])}) "
            f"и постоянных издержек в {data['FC_total']} руб. "
            f"(включая: {', '.join([f'{name} ({cost} руб.)' for name, cost in data['FC_info']])}), "
            f"прибыль составит: "
            f"{data['P'] * data['Q'] - data['FC_total'] - data['VC_total'] * data['Q']} руб."
        )

        # Отправляем ответ пользователю
        await message.answer(response, reply_markup=reply.main)

        # Сбрасываем состояние
        await state.clear()
    except ValueError:
        await message.answer("Пожалуйста, введите целое число.")
