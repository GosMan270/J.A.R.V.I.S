from fastapi import FastAPI

from voice_asistent.core.program import JARVIS
from utils.database import DATABASE

from core.tts import router as tts_router
from core.stt import router as stt_router

app = FastAPI()


app.include_router(stt_router)
app.include_router(tts_router)


@app.on_event("startup")
async def startup_event():
    await JARVIS.run()


@app.on_event("shutdown")
async def shutdown_event():
    await DATABASE.close_connection()
