
from VoiceAssistent.modul.router.ai.handler import handle as AI
from .src.data.map import FitnessTrainerPrompt

async def handle(text):
    message = text
    system = FitnessTrainerPrompt
    res = await AI(message, system)
    return res