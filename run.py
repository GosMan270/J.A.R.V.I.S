import sys
import asyncio
import logging
from src.program import Jarvis
from src.run.config import config
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    while True:
        try:
            jarvis = Jarvis()
            asyncio.run(jarvis.run())
        except Exception as e:
            print(f"Jarvis упал с ошибкой: {e}")
            print("Перезапуск через 2 секунды...")
            time.sleep(2)
        else:
            # Если вышли без ошибок (например, по Ctrl+C), можно выйти из цикла
            print("Jarvis завершён корректно.")
            break