"""
Файл запуска,и активации ивента
"""
from fastapi import FastAPI

from core.program import router as core_router
from modul.commands_center import router as command_center_router

from VoiceAssistent.core.program import JARVIS



app = FastAPI()


app.include_router(core_router)
app.include_router(command_center_router)


@app.on_event("startup")
async def startup_event():
    """
    Ивент запуска
    """
    await JARVIS.run()


@app.on_event("shutdown")
async def shutdown_event():
    """
    Ивент завершения работы
    """
    await DATABASE.close_connection()





import asyncio
import time
import threading

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from rq import Queue
from redis import Redis

app = FastAPI()

# 1. Настроим соединение с Redis и очередь RQ.
redis_conn = Redis()
q = Queue(connection=redis_conn)

# 2. Хранилище сопоставления job_id <-> websocket
active_ws_by_job = {}


# 3. Пример тяжелой задачи (RQ таска)
def heavy_ai_task(user_text):
    time.sleep(3)  # Симуляция долгой работы
    return f"Ответ готов: {user_text[::-1]}"


# 4. Вебсокет эндпоинт
@app.websocket("/ws/ai/{user_id}")
async def ai_ws(websocket: WebSocket, user_id: int):
    await websocket.accept()
    print("connection open")

    try:
        while True:
            data = await websocket.receive_json()
            user_text = data["text"]

            # Кладем задачу в очередь RQ и сохраняем связь
            job = q.enqueue(heavy_ai_task, user_text)
            active_ws_by_job[job.id] = websocket

            # Возвращаем job_id клиенту
            await websocket.send_json({"job_id": job.id})

    except WebSocketDisconnect:
        print("connection closed")
        # Удалить все связанные job_id для этого websocket
        to_delete = [jid for jid, ws in active_ws_by_job.items() if ws == websocket]
        for jid in to_delete:
            del active_ws_by_job[jid]


# 5. Поток-отправитель результата в основной event loop
def result_sender(loop):
    from rq.job import Job

    while True:
        to_del = []
        for job_id, ws in list(active_ws_by_job.items()):
            try:
                job = Job.fetch(job_id, connection=redis_conn)
                if job.is_finished:
                    # Шлем результат через основной event loop сервера
                    future = asyncio.run_coroutine_threadsafe(
                        ws.send_json({"job_id": job_id, "result": job.result}),
                        loop
                    )
                    try:
                        future.result()  # Ждем завершения
                    except Exception as e:
                        print(f"Ошибка отправки ws: {e}")
                    to_del.append(job_id)
            except Exception as ex:
                print(f"Error checking job_id={job_id} — {ex}")
                to_del.append(job_id)
        for jid in to_del:
            active_ws_by_job.pop(jid, None)
        time.sleep(0.5)


# 6. Стартуем поток result_sender при старте приложения
@app.on_event("startup")
async def startup_event():
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=result_sender, args=(loop,), daemon=True)
    t.start()
    print("Result sender thread started!")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
