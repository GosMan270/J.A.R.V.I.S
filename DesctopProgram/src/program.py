"""
Файл инициализации и запуска моделей Vosk Silero TTS А так же подключение к Базе данных
"""

import logging
import os

import pvporcupine
import pyaudio
import torch
import vosk
import fastapi

from fastapi import FastAPI
from dotenv import load_dotenv

from src.data.voice import Voice
from src.data.database import DATABASE


logging.basicConfig(level=logging.INFO)

dotenv_path = os.path.join(os.path.dirname(__file__), 'data', 'run', 'config.env')
load_dotenv(dotenv_path)


class Jarvis:
    """
    Класс инициализирует и загружает модели Vosk Silero TTS. А так же подключение к Базе данных
    """
    def __init__(self):
        """
        Инициализация и загрузка ИИ
        """
        # Инициализация PICO
        self.porcupine = pvporcupine.create(
            access_key=os.getenv('PICO_KEY'),
            keyword_paths=[os.getenv("PICO_MODEL")]
        )

        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        logging.info(os.getenv('PICO_MODEL') + ' loaded is grate ')

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

        # Передача в класс Voice в src.data.voice
        self.VOICE = Voice(
            self.porcupine,
            self.pa,
            self.audio_stream,
            self.silero_model,
            self.rec,
            self.language,
            self.model_id,
            self.speaker,
            self.device,
            self.tts_sample_rate,
            context=self
        )


    async def run(self):
        """
        Запуск основной функции
        """
        #захардкодил path. Временное решение. Потом перенесется в config.env
        #при переходе на посгре и композ
        await DATABASE.open_connection('C:/coding/PROGRAM/jarvis/VoiceAssistent/identifier.sqlite')
        await self.VOICE.search_wwd()


JARVIS = Jarvis()
