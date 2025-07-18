"""
Файл инициализации и запуска моделей Vosk Silero TTS А так же подключение к Базе данных. По совместительству ядро
"""
import logging
import os
import json
import asyncio
import torch
import vosk
import inspect
import io

import numpy as np
import soundfile as sf

from enum import Enum
from fastapi import APIRouter, UploadFile
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from pydantic import BaseModel

from VoiceAssistent.utils.database import DATABASE



logging.basicConfig(level=logging.INFO)


dotenv_path = os.path.join(os.path.dirname(__file__), 'data', 'run', 'config.env')


load_dotenv(dotenv_path)


router = APIRouter()


class TtsRequest(BaseModel):
    text: str


class Jarvis:
    """
    Класс инициализирует и загружает модели Vosk Silero TTS. А так же подключение к Базе данных/Ядро ассистента
    """
    def __init__(self):
        """
        Инициализация и загрузка ИИ
        """
        # Инициализация VOSK
        if not os.path.exists(os.getenv('VOSK_MODEL')):
            print("Dont model!")
            exit(1)
        self.vosk_model = vosk.Model(os.getenv('VOSK_MODEL'))
        self.rec = vosk.KaldiRecognizer(
            self.vosk_model,
            int(os.getenv('VOSK_FRAME_RATE'))
        )
        print("VOSK LOADED!")

        # Инициализация SILERO
        self.language = "ru"
        self.model_id = "ru_v3"
        self.speaker = "baya"
        self.tts_sample_rate = 48000
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.silero_model, _ = torch.hub.load(
            'snakers4/silero-models',
            'silero_tts',
            language=self.language,
            speaker=self.model_id
        )
        print("Доступные голоса:", self.silero_model.speakers)
        if self.speaker not in self.silero_model.speakers:
            raise ValueError(f"Голос {self.speaker} не найден! Используй один из: {self.silero_model.speakers}")


    async def run_db(self):
        """
        Запуск BD
        """
        await DATABASE.open_connection('C:/coding/PROGRAM/jarvis/VoiceAssistent/identifier.sqlite')


    def tts_generate_sync(self, text):
        """
        Синхронно озвучивает текст (используется внутри voice_generate).
        Поддерживает разные сигнатуры TTS моделей (может быть text или texts).

        Args:
            text (str): Текст для озвучивания.
        """
        sig = inspect.signature(self.silero_model.apply_tts)
        if 'texts' in sig.parameters:
            audio = self.silero_model.apply_tts(
                texts=[text],
                speaker=self.speaker,
                sample_rate=self.tts_sample_rate
            )[0]
        else:
            audio = self.silero_model.apply_tts(
                text=text,
                speaker=self.speaker,
                sample_rate=self.tts_sample_rate
            )
        if hasattr(audio, "cpu"):
            audio = audio.cpu().numpy()
        audio = audio.astype('float32')
        buffer = io.BytesIO()
        sf.write(buffer, audio, self.tts_sample_rate, format='WAV')
        buffer.seek(0)
        return buffer


    def stt_generate_sync(self, audio_file):
        self.rec.AcceptWaveform(audio_file)
        result = json.loads(self.rec.Result())
        phrase = result.get('text')
        logging.info(f'распознано: {phrase}')
        return phrase


@router.post('/tts')
async def tts_generate(tts_request: TtsRequest):
    """
    Запрос на синтез голоса silero tts
    :param tts_request: {text: str}
    :return: tts.wav
    """
    loop = asyncio.get_running_loop()
    audio_buffer = await loop.run_in_executor(None, JARVIS.tts_generate_sync, tts_request.text)
    return StreamingResponse(
        audio_buffer,
        media_type="audio/wav",
        headers={
            "Content-Disposition": 'attachment; filename="tts.wav"'
        }
    )


@router.post('/stt')
async def stt_generate(file: UploadFile):
    """
    Запрос для перевода голоса в текст
    :param (file: UploadFile (Отправить аудио файл))
    :return: (text: str)
    """
    audio_file = file.file
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, JARVIS.stt_generate_sync, audio_file)

    return {
        "status": "True",
        'result': result
    }


JARVIS = Jarvis()





