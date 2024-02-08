from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text.lower().in_(["4 задача"]))
async def handle_problem4(message: Message):
    # Implement logic for problem 4 here
    await message.reply("This is problem 4 handler.")