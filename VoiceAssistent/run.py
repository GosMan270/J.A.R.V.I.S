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
