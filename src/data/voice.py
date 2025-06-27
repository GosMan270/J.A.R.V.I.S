import asyncio
import numpy as np
import soundfile as sf
import vlc
import time
import json
import inspect
import random
import sounddevice as sd

from src.data.run.prompt import standart_word
from src.command.commands_center import COMMANDS_CENTER




def is_silence(audio_bytes, threshold=500):
    arr = np.frombuffer(audio_bytes, dtype=np.int16)
    if arr.size == 0:
        return True
    return np.abs(arr).mean() < threshold



class Voice:
	def __init__(self, porcupine, pa, audio_stream, model, rec, language, model_id, speaker, device, sample_rate, context=None):
		self.porcupine = porcupine
		self.pa = pa
		self.audio_stream = audio_stream
		self.model = model
		self.rec = rec
		self.language = language
		self.model_id = model_id
		self.speaker = speaker
		self.device = device
		self.sample_rate = sample_rate
		self.context = context
		
		
		
	async def search_wwd(self):
		await self.voice_generate(random.choice(standart_word['system']))
		try:
			while True:
				pcm = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
				arr = np.frombuffer(pcm, dtype=np.int16)
				res = self.porcupine.process(arr)
				if res >= 0:
					await self.voice_generate("Слушаю сэр...")
					await asyncio.sleep(1)
					await self.response(2)
		except KeyboardInterrupt:
			print("Останавливаемся...")
		finally:
			self.audio_stream.close()
			self.pa.terminate()
			self.porcupine.delete()
	
	
	
	async def response(self, lag: int, as_phrase: bool = False):
		frames = []
		silence_max = (lag * int(16000 / self.porcupine.frame_length))
		silence_count = 0
		while True:
			data = self.audio_stream.read(self.porcupine.frame_length, exception_on_overflow=False)
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
		if as_phrase:
			return phrase
		else:
			await COMMANDS_CENTER.command_center(phrase, self.context)

	
	async def voice_generate(self, text):
		loop = asyncio.get_running_loop()
		await loop.run_in_executor(None, self._voice_generate_sync, text)
	
	def _voice_generate_sync(self, text):
		sig = inspect.signature(self.model.apply_tts)
		if 'texts' in sig.parameters:
			audio = self.model.apply_tts(
				texts=[text],
				speaker=self.speaker,
				sample_rate=self.sample_rate
			)[0]
		else:
			audio = self.model.apply_tts(
				text=text,
				speaker=self.speaker,
				sample_rate=self.sample_rate
			)
		# Нормализуем, если требуется
		audio = audio.astype('float32')  # sounddevice ожидает float32
		sd.play(audio, self.sample_rate)
		sd.wait()  # дождаться окончания воспроизведения

