from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards import reply

router = Router()


@router.message(CommandStart())
async def start(message: Message):
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
    await state.clear()
    await message.answer(
        text="Задача отменена",
        reply_markup=reply.main
    )

# @router.message(commands=['cancel'])
# async def cancel(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Операция отменена. Выберите задачу из списка.", reply_markup=reply.main)
