
from VoiceAssistent.modul.router.ai.handler import handle as AI
from .src.data.map import FitnessTrainerPrompt, AudioFitnessTrainerPrompt



async def handle(text):
    res = []

    #параметры для промпта
    user_text = text
    system = FitnessTrainerPrompt

    #добавление в список текстовой версии для вывода
    message = await AI(user_text, system)
    res.append(message)

    #Новые параметры для промпта
    text = message
    system = AudioFitnessTrainerPrompt
    #добавление версии для озвучки
    audio_message = await AI(text, system)
    res.append(audio_message)
    return res


# class ai_definition:

















