from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart

from src.router.jarvis import control as controller
from src.router.jarvis import view as viewer

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    view = viewer.start(message)
    await message.answer(f"{view[0]}", parse_mode="Markdown")