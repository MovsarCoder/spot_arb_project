from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("information"))
async def information_command(message: Message):
    await message.answer("Скоро будет доступно!")
