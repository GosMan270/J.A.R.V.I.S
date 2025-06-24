import os
import importlib

from .map import COMMAND_MAPPINGS





class CommandCenter:
    def __init__(self, router_path="src.command.router"):
        self.handlers = {}
        router_folder = os.path.join(os.path.dirname(__file__), "router")
        for dirname in os.listdir(router_folder):
            dirpath = os.path.join(router_folder, dirname)
            if os.path.isdir(dirpath):
                handler_path = os.path.join(dirpath, "handler.py")
                if os.path.exists(handler_path):
                    module_name = f"{router_path}.{dirname}.handler"
                    try:
                        module = importlib.import_module(module_name)
                        self.handlers[dirname] = module.handle
                    except Exception as e:
                        print(f"Не удалось загрузить роутер {dirname}: {e}")
    
    async def command_center(self, text, context):
	    norm_text = text.lower()
	    mapped_cmd = None
	    
	    for key_phrases, handler_name in COMMAND_MAPPINGS.items():
		    if any(phrase in norm_text for phrase in key_phrases):
			    mapped_cmd = handler_name
			    break
	    
	    if mapped_cmd and mapped_cmd in self.handlers:
		    try:
			    await self.handlers[mapped_cmd](text, context)
		    except Exception as e:
			    print(f"Ошибка в обработчике {mapped_cmd}: {e}")
		    return
	    
	    print("Неизвестная команда:", text)
	    
	    
COMMANDS_CENTER = CommandCenter()
	    
		