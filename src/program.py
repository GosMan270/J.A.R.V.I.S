import pvporcupine
import pyaudio
import asyncio
import numpy as np
import json
import os
import vosk
import vlc

from src.data.utils import VOICE
from src.run.config import config
from src.data.utils import AI

def is_silence(audio_bytes, threshold=500):
    arr = np.frombuffer(audio_bytes, dtype=np.int16)
    if arr.size == 0:
        return True
    return np.abs(arr).mean() < threshold

class Jarvis:
    def __init__(self):
        print("JARVIS initialization....")
        self.porcupine = pvporcupine.create(
            access_key=config['pico_key'],
            keyword_paths=[config['pico_model']],
        )
        print("Porcupine initialization....")
        self.pa = pyaudio.PyAudio()
        print("Pa initialization....")
        self.audio_stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )
        print("Audio stream initialization...")
        if not os.path.exists(config['vosk_model']):
            print("Dont model!")
            exit(1)
        print("Model loaded....")
        self.model = vosk.Model(config['vosk_model'])
        print("Model successfully loaded!")
        self.rec = vosk.KaldiRecognizer(self.model, config['vosk_frame_rate'])
        print("Model and rec grate loaded!")


    async def run(self):
        try:
            while True:
                pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                arr = np.frombuffer(pcm, dtype=np.int16)
                res = self.porcupine.process(arr)
                if res >= 0:
                    asyncio.create_task(VOICE.voice_generate("Слушаю сэр"))
                    await asyncio.sleep(1)
                    
                    frames = []
                    silence_count = 0
                    silence_max = (2 * int(16000 / self.porcupine.frame_length))
                    while True:
                        data = self.audio_stream.read(pcm)
                        frames.append(data)
                        if is_silence(data):
                            silence_count += 1
                        else:
                            silence_count = 0
                        if silence_count >= silence_max:
                            break
                    audio_data = b''.join(frames)

                    self.rec.AcceptWaveform(audio_data)
                    result = json.loads(self.rec.Result())
                    phrase = result.get('text')
                    print("Распознано:", phrase)
                    
                    if "папочка вернулся" or "я дома" in phrase.lower():
                        await self.command_hello()
                        
                    else:
                        res = await AI.OpenAi(phrase, "Отвечай ТОЛЬКО ПО ДЕЛУ! И НИЧЕГО ЛИШНЕГО! Должно быть коротко, ясно, официально и с уважением.")
                        try:
                            answer_text = res
                        except Exception:
                            answer_text = str(res)
                        await VOICE.voice_generate(answer_text)

        except KeyboardInterrupt:
            print("Останавливаемся...")
        finally:
            self.audio_stream.close()
            self.pa.terminate()
            self.porcupine.delete()

          
          
    async def command_hello(self):
        res = await AI.OpenAi("мне нужно ТОЛЬКО ПРИВЕТСТВИЕ И НИЧЕГО БОЛЬШЕ. Оно должно быть в стиле джарвис из железного человека. Что то типа 'С возвращением, сер' или 'Рад что вы вернули сер' или 'К вашим услугам сер' В ОБЩЕМ КАКОЕ ТО ПРИВЕТСТВИЕ", config['standart_sp'])
        player = vlc.MediaPlayer("D:/work/coding/O.S.C.A.R/system/sound/AC_DC - Back In Black.mp3")
        player.play()
        await asyncio.sleep(1)
        await VOICE.voice_generate(res)