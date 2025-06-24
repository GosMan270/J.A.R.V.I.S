import asyncio
import logging
from src.program import Jarvis
import time
import traceback


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    while True:
        try:
            jarvis = Jarvis()
            asyncio.run(jarvis.run())
        except Exception as e:
            print(f"Jarvis упал с ошибкой: {e}")
            traceback.print_exc()
            print("Перезапуск через 2 секунды...")
            time.sleep(2)
        else:
            print("Jarvis завершён корректно.")
            break