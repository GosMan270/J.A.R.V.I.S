import os
import vosk
import json
import aiohttp
import asyncio
import pyttsx3
import pvporcupine
import pyaudio
import numpy as np

from src.run.config import config


class Voice:
	def __init__(self):
		pass
	
	
	async def voice_generate(self, text):
		loop = asyncio.get_event_loop()
		await loop.run_in_executor(None, self._voice_generate_sync, text)
	
	
	def _voice_generate_sync(self, text):
		engine = pyttsx3.init('sapi5')
		voices = engine.getProperty('voices')
		
		russian_voice = None
		for v in voices:
			if 'ru' in str(v.languages).lower() or 'russian' in v.name.lower():
				russian_voice = v
				break
		if russian_voice:
			engine.setProperty('voice', russian_voice.id)
		engine.setProperty('rate', 170)  # Можно изменить скорость
		clean_text = text.replace('\n', ' ')
		engine.say(clean_text)
		engine.runAndWait()




class Ai:
	def __init__(self):
		pass
	
	
	async def _do_http_request(self, url, data):
		headers = {
			"Authorization": f"Bearer {config["api_key"]}",
			"Content-Type": "application/json"
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(url, headers=headers, json=data) as response:
				j = await response.json()
				if "id" in j and "error" in j["id"]:
					raise Exception(json.dumps(j))
				return j
	
	
	async def OpenAi(self, text, system):
		data = {
			"model": "gpt-4.1",
			"max_tokens": 4048,
			"messages":[
				{
					"role": "user",
					"content": text
				},
				{
					"role": "system",
					"content": system
				}
			]
		}
		res = await self._do_http_request(config["api_url"], data)
		return res['choices'][0]['message']['content']



AI = Ai()
VOICE = Voice()
