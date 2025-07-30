import asyncio
from rq import Queue
from redis import Redis
import threading

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException, FastAPI
from typing import Dict

from .map import CM, PROMPTS, PromptSelectSystem

#Модули
from .router.ai.handler import handle as AI
from .router.coach.handler import handle as MyCoach



app = FastAPI()
redis_conn = Redis()
q = Queue(connection=redis_conn)


"""Список доступных модулей из импорта"""
hendlers = {
    'AI': AI,
    'MyCoach': MyCoach
}


"""Активные API_KEY из WebSocket"""
active_ws_by_job = {}



class ConnectionManager:


    def __init__(self):
        """Хранение активных соединений в виде {room_id: {user_id: WebSocket}}"""
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}


    async def connect(self, websocket: WebSocket, room_id: int, user_id: int):
        """
        Устанавливает соединение с пользователем.
        websocket.accept() — подтверждает подключение.
        """
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = {}
        self.active_connections[room_id][user_id] = websocket


    def disconnect(self, room_id: int, user_id: int):
        """
        Закрывает соединение и удаляет его из списка активных подключений.
        Если в комнате больше нет пользователей, удаляет комнату.
        """
        if room_id in self.active_connections and user_id in self.active_connections[room_id]:
            del self.active_connections[room_id][user_id]
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]


    async def broadcast(self, message: str, room_id: int, sender_id: int):
        """
        Рассылает сообщение всем пользователям в комнате.
        """
        if room_id in self.active_connections:
            for user_id, connection in self.active_connections[room_id].items():
                message_with_class = {
                    "text": message,
                    "is_self": user_id == sender_id
                }
                await connection.send_json(message_with_class)



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
        if isinstance(ai_command, Exception):
            # можно залогировать и вернуть фразу или raise HTTPException
            print(f"AI detect_command выкинул exception: {ai_command}")
            raise HTTPException(status_code=500, detail=f"AI detect_command error: {ai_command}")
        else:
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














from fastapi.responses import HTMLResponse


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/1/2");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/ws/{key}/{device}")
async def websocket_endpoint(websocket: WebSocket, key: str, device: str):
    key = 123
    device = 123
    await manager.connect(websocket, key, device)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"MESSAGE = {data}", key, device)
    except WebSocketDisconnect:
        manager.disconnect(key, device)
        await manager.broadcast(f"(ID: {device}) покинул чат.", key, device )


async def heavy_ai_task(user_text):
    """Запуск задачи"""
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


def result_sender(loop):
    """Возвращение результата"""
    from rq.job import Job
    import time
    while True:
        for job_id, ws in list(active_ws_by_job.items()):
            job = Job.fetch(job_id, connection=redis_conn)
            if job.is_finished:
                future = asyncio.run_coroutine_threadsafe(
                    ws.send_json({'job_id': job_id, 'result': job.result}),
                    loop
                )
                try:
                    future.result()  # можно ждать, можно не ждать
                except Exception as e:
                    print("Ошибка при отправке ws:", e)
                del active_ws_by_job[job_id]
        time.sleep(0.5)


@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_running_loop()
    threading.Thread(target=result_sender, args=(loop,), daemon=True).start()


manager = ConnectionManager()
COMMAND_CENTER = CommandCenter()