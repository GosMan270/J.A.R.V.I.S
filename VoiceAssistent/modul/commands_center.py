import os
import importlib
import asyncio

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .map import CM, PROMPTS, PromptSelectSystem

#Модули
from .router.ai.handler import handle as AI



app = FastAPI()



hendler = {
    'AI': AI,
}



class CommandRequest(BaseModel):
    text: str



class CommandCenter:


    async def detect_command(self, user_text):
        """Первый этап: AI пытается найти команду."""
        return await AI(user_text, CM.command_map() if callable(CM.command_map) else CM)


    async def detect_prompt(self, user_text):
        """Второй этап: попытка определить нужный промпт."""
        res = await AI(user_text, PromptSelectSystem)
        if res in PROMPTS:
            return res
        return "standart"


    async def run_handler(self, handler, user_text, context=None):
        if context is not None:
            return await handler(user_text, context)
        else:
            return await handler(user_text)


    async def general_ai(self, user_text, prompt_name):
        """Дать ответ через выбранный промпт."""
        prompt = PROMPTS.get(prompt_name, PROMPTS['standart'])
        return await AI(user_text, prompt)


    async def command_center(self, user_text, context=None):
        self.load_routers()
        norm_text = user_text.lower()
        mapped_cmd = None

        for key_phrases, handler_name in (CM.command_map() if callable(CM.command_map) else CM).items():
            if any(phrase in norm_text for phrase in key_phrases):
                mapped_cmd = handler_name
                break

        if mapped_cmd and mapped_cmd in self.handlers:
            try:
                return await self.run_handler(self.handlers[mapped_cmd], user_text, context)
            except Exception as e:
                print(f"Ошибка в обработчике {mapped_cmd}: {e}")


COMMAND_CENTER = CommandCenter()


@app.post('/command')
async def command(command_request: CommandRequest) -> dict:
    user_text = command_request.text.strip()
    try:
        # стартуем три корутины одновременно!
        coro1 = COMMAND_CENTER.detect_command(user_text)
        coro2 = COMMAND_CENTER.detect_prompt(user_text)
        coro3 = COMMAND_CENTER.general_ai(user_text, "standart")

        results = await asyncio.gather(
            coro1,  # ai_command
            coro2,  # prompt_name
            coro3,  # ai general answer
            return_exceptions=True
        )

        # results[0] = вывод detect_command
        # results[1] = detect_prompt
        # results[2] = general_ai

        return {
            "ai_command": results[0],
            "prompt_name": results[1],
            "ai_answer": results[2]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))