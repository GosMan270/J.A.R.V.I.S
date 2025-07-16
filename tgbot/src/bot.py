import aiogram
import asyncio
import os

from dotenv import load_dotenv
from aiogram import types, Bot, dispatcher, Dispatcher

from src.router.jarvis.module import router as jarvis_router

class TgBot:
    def __init__(self):
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'run', 'config.env')
        print("dotenv_path", dotenv_path)
        load_dotenv(dotenv_path)

        self.tg_bot_key = str(os.getenv('tg_bot_key'))
        self.bot: Bot = None
        self.dispatcher: Dispatcher = None

    async def run(self):
        self.bot = aiogram.Bot(self.tg_bot_key)
        self.dispatch = aiogram.Dispatcher()

        self.dispatch.include_router(jarvis_router)

        await self.dispatch.start_polling(self.bot)
