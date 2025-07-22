import os
import importlib
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .map import CM, PROMPTS, PromptSelectSystem

#Модули
from .router.ai.handler import handle as AI




app = FastAPI()



hendlers = {
    'AI': AI
}



class CommandRequest(BaseModel):
    text: str



class CommandCenter:
    """Класс распределения команд"""


    async def detect_command(self, user_text):
        """Первый этап: AI пытается найти команду."""
        return await AI(user_text, CM.command_map())


    async def detect_prompt(self, user_text):
        """Второй этап: попытка определить нужный промпт."""
        res = await AI(user_text, PromptSelectSystem)
        if res in PROMPTS:
            return res
        return "standart"


    async def general_ai(self, user_text, prompt_name):
        """Дать ответ через выбранный промпт."""
        prompt = PROMPTS.get(prompt_name, PROMPTS['StandartPrompt'])
        return await AI(user_text, prompt)


    async def ai_final_answer(self,user_text, ai_command, prompt_name, ai_answer):
        """Анализ всех 3 вызовов и конечный результат"""
        if ai_command == 'def_None':
            return ai_answer
        elif ai_command != 'def_None':
            return await self.command_center(user_text, ai_command)


    async def command_center(self, user_text, ai_command):
        name_hendler = ai_command.split('_')[1]
        print(name_hendler)

        if name_hendler in hendlers:
            print(hendlers)
            try:
                return await self.run_handler(hendlers[name_hendler], user_text)
            except Exception as e:
                print(f"Ошибка в обработчике {name_hendler}: {e}")
        else:
            return f"error 5XX. the module {name_hendler} is missing"

    async def run_handler(self, handler, user_text):
            return await handler(user_text)


COMMAND_CENTER = CommandCenter()


@app.post('/command')
async def command(command_request: CommandRequest) -> dict:
    user_text = command_request.text.strip()
    try:
        # стартуем три корутины одновременно!
        coro1 = COMMAND_CENTER.detect_command(user_text)
        coro2 = COMMAND_CENTER.detect_prompt(user_text)
        coro3 = COMMAND_CENTER.general_ai(user_text, "StandartPrompt")


        results = await asyncio.gather(
            coro1,  # ai_command
            coro2,  # prompt_name
            coro3,  # ai general answer
            return_exceptions=True
        )



        # results[0] = вывод detect_command
        # results[1] = detect_prompt
        # results[2] = general_ai
        res = await  COMMAND_CENTER.ai_final_answer(user_text, results[0], results[1], results[2])


        return {
            "ai_command": results[0],
            "prompt_name": results[1],
            "ai_answer": results[2],
            "ai_final_answer": res,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))