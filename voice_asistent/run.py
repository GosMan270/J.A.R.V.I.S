"""
Запуск ассистента
"""
import asyncio
import traceback

from src.program import Jarvis
from src.data.database import DATABASE




async def start():
    while True:
        try:
            jarvis = Jarvis()
            await jarvis.run()
        except Exception as e:
            print(f"Отключен с ошибкой: {e}")
            traceback.print_exc()
            print("Перезапуск через 2 секунды...")
            await DATABASE.close_connection()
            await asyncio.sleep(2)
        else:
            print("Jarvis завершён корректно.")
            await DATABASE.close_connection()
            break

if __name__ == "__main__":
    asyncio.run(start())