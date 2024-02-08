from aiogram import Router, F
from aiogram.types import Message

from keyboards import reply, inline, builders, fabrics
from data.subloader import get_json

router = Router()


@router.message(F.text.lower().in_(["хай", "хеллоу", "привет"]))
async def greeting(message: Message):
    await message.reply("Привееет!^^")


@router.message()
async def echo(message: Message):
    msg = message.text.lower().strip()
    smiles = await get_json("smiles.json")

    if msg == "1 задача":
        await message.answer("Описание для 1 задачи ?", reply_markup=reply.problem1_keyboard)
    elif msg == "спец. кнопки":
        await message.answer("Спец. кнопки:", reply_markup=reply.spec)
    elif msg == "калькулятор":
        await message.answer("Введите выражение:", reply_markup=builders.calc())
    elif msg == "смайлики":
        await message.answer(f"{smiles[0][0]} <b>{smiles[0][1]}</b>", reply_markup=fabrics.paginator())
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!", reply_markup=reply.main)
