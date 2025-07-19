import os
import importlib

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .map import CM, PROMPTS, PromptSelectSystem



app = FastAPI()


class CommandRequest(BaseModel):
    text: str


class CommandCenter:
    def __init__(self, router_path="VoiceAssistent.modul.router"):
        self.router_path = router_path
        self.router_folder = os.path.join(os.path.dirname(__file__), "router")
        self.handlers = {}
        self.load_routers()


    def load_routers(self):
        self.handlers.clear()
        for dirname in os.listdir(self.router_folder):
            dirpath = os.path.join(self.router_folder, dirname)
            if os.path.isdir(dirpath):
                handler_path = os.path.join(dirpath, "handler.py")
                if os.path.exists(handler_path):
                    module_name = f"{self.router_path}.{dirname}.handler"
                    try:
                        if module_name in importlib.sys.modules:
                            module = importlib.reload(importlib.sys.modules[module_name])
                        else:
                            module = importlib.import_module(module_name)
                        self.handlers[dirname] = module.handle
                    except Exception as e:
                        print(f"Не удалось загрузить роутер {dirname}: {e}")


    async def detect_command(self, user_text):
        """Первый этап: AI пытается найти команду."""
        return await self.handlers['ai'](user_text, CM.command_map() if callable(CM.command_map) else CM)


    async def detect_prompt(self, user_text):
        """Второй этап: попытка определить нужный промпт."""
        res = await self.handlers['ai'](user_text, PromptSelectSystem)
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
        return await self.handlers['ai'](user_text, prompt)


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

        # fallback: AI
        try:
            return await self.run_handler(self.handlers["ai"], user_text, context)
        except Exception as e:
            print(f"Ошибка в AI обработчике: {e}")


COMMAND_CENTER = CommandCenter()


@app.post('/command')
async def command(command_request: CommandRequest) -> dict:
    user_text = command_request.text.strip()
    try:
        # AI пытается найти команду (возвращает строку типа "def_<name function>")
        ai_command = await COMMAND_CENTER.detect_command(user_text)
        if ai_command and ai_command.startswith("def_"):
            function_name = ai_command[4:].strip().lower()
            handler = COMMAND_CENTER.handlers.get(function_name)
            if handler:
                result = await COMMAND_CENTER.run_handler(handler, user_text)
                return {"result": result}
        # Если не найдено, ищем промпт
        prompt_name = await COMMAND_CENTER.detect_prompt(user_text)
        result = await COMMAND_CENTER.general_ai(user_text, prompt_name)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))