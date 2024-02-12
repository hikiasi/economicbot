"""
Этот модуль содержит обработчики для пользовательских команд, таких как /start и /cancel.
"""

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards import reply

router = Router()


@router.message(CommandStart())
async def start(message: Message):

    """
    Обрабатывает команду /start.
    Отправляет приветственное сообщение пользователю с кратким описанием доступных задач

    Args:
        message (Message): Объект сообщения.

    Returns:
        None
    """

    user_name = message.from_user.first_name

    greeting_text = (
        f"Привет, <b>{user_name}</b>! 🌟 Это бот, который поможет тебе решать задачи по экономической теории. "
        "Спасибо, что решил воспользоваться нашим сервисом! Вот задачи, которые мы можем решить:\n\n"
        "<b>1) Построение общей КПВ:</b>\n"
        "   Вводи максимальный объем производства товаров А и Б для 1 и 2 производителя, "
        "а мы построим график общей КПВ!\n\n"
        "<b>2) Нахождение точки рыночного равновесия:</b>\n"
        "   По определенным формулам и твоим данным, мы посчитаем параметры равновесия в считанные секунды.\n\n"
        "<b>3) Расчет объема дефицита/излишка:</b>\n"
        "   Получи ответ о ситуации на рынке при уровне цены в определенное количество денежных единиц.\n\n"
        "<b>4) Расчет прибыли фирмы:</b>\n"
        "   Узнай, сколько составит прибыль при реализации продукции. Мы готовы помочь!"
    )

    await message.answer(greeting_text, reply_markup=reply.main)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "отмена")
async def cmd_cancel(message: Message, state: FSMContext):

    """
    Обрабатывает команду /cancel и сообщение "Отмена"
    Очищает текущее состояние и отправляет сообщение о подтверждении отмены

    Args:
        message (Message): Объект сообщения.
        state (FSMContext): Объект FSMContext.

    Returns:
        None
    """

    await state.clear()
    await message.answer(
        text="Задача отменена",
        reply_markup=reply.main
    )
