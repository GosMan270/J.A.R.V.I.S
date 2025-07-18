"""
Файл запуска REST с ивентами
"""
from fastapi import FastAPI

from core.program import router as core_router

from voice_asistent.core.program import JARVIS
from utils.database import DATABASE



app = FastAPI()


app.include_router(core_router)


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
