from aiogram import Router
from aiogram.types import Message
from aiogram import F

router = Router()

@router.message(F.voice)
async def voice(message: Message):
    pass

@router.message()
async def incorrect(message: Message):
    message.answer("Incorrect Message, only voice")