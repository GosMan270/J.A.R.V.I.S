"""
Файл загрузки модулей для взаимодействия с ядром ассистента
"""
import os
import importlib
import sys
import logging
import asyncio

from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

from .router.ai.handler import handle

from .map import CM
# from modul.map import COMMAND_MAPPINGS


# router = APIRouter()
app = FastAPI()


logging.basicConfig(level=logging.INFO)


class CommandRequest(BaseModel):
    text: str


class CommandCenter:
    """
    Класс для распределения команд и автоматической подгрузки модулей
    """
    async def responce_ai(self, text, system):
        norm_text = text.lower()
        try:
            print(system)
            res = await handle(norm_text, system)

            return res
        except Exception as e:
            print(f"Ошибка в AI обработчике: {e}")


    async def command_center(self, text):
        pass





@app.post('/command')
async def command(command_request: CommandRequest) -> dict:
    """
    Обрабатывает пользовательскую команду для виртуальной помощницы J.A.R.V.I.S.
    """
    try:
        res = await COMMANDS_CENTER.responce_ai(command_request.text, str(CM.command_map()))
        return {'result': res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


COMMANDS_CENTER = CommandCenter()
