import pvporcupine
import pyaudio
import os
import vosk
import random

import torch

from src.data.utils import CHECKS
from src.data.run.config import config
from src.data.run.prompt import standart_word
from src.data.voice import Voice





class Jarvis:
    #Инициализация моделей ИИ и загрузка
    def __init__(self):
        
        #Инициализация PICO
        self.porcupine = pvporcupine.create(
            access_key=config['pico_key'],
            keyword_paths=[config['pico_model']],
        )
        print("PICO LOADED!")

        #Инициализация VOSK
        self.pa = pyaudio.PyAudio()
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        if not os.path.exists(config['vosk_model']):
            print("Dont model!")
            exit(1)
        self.model = vosk.Model(config['vosk_model'])
        self.rec = vosk.KaldiRecognizer(self.model, config['vosk_frame_rate'])
        print("VOSK LOADED!")

        # Инициализация SILERO
        self.language = "ru"
        self.model_id = "ru_v3"
        self.speaker = "baya"
        self.sample_rate = 48000
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, _ = torch.hub.load(
            'snakers4/silero-models',
            'silero_tts',
            language=self.language,
            speaker=self.model_id
        )
        print("Доступные голоса:", self.model.speakers)
        if self.speaker not in self.model.speakers:
            raise ValueError(f"Голос {self.speaker} не найден! Используй один из: {self.model.speakers}")
        
        #Передача в класс Voice в src.data.voice
        self.VOICE = Voice(
            self.porcupine,
            self.pa,
            self.audio_stream,
            self.model,
            self.rec,
            self.language,
            self.model_id,
            self.speaker,
            self.device,
            self.sample_rate,
            context = self
        )
    
    
    #проверка wifi
    async def сhecks(self):
        if CHECKS.is_connected():
            config['wifi'] = True
        else:
            config['wifi'] = False
            await self.VOICE.voice_generate(random.choice(standart_word['no_wifi']))

    
    async def run(self):
        await self.сhecks()
        await self.VOICE.search_wwd()
        
    
    
    
JARVIS = Jarvis()
