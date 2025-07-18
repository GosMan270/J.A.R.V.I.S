"""
Файл запроса к ии на внешний API
"""
import aiohttp
import json
import asyncio
import dotenv
import os

from dotenv import load_dotenv



dotenv_patch = os.path.join(os.path.dirname(__file__),'run', '.env')
load_dotenv(dotenv_patch)

class Ai:
	def __init__(self):
		self.dotenv_patch = os.path.join(os.path.dirname(__file__), 'run', '.env')
		load_dotenv(self.dotenv_patch)
	
	
	async def handle(self, text, context):
		res = await self.open_ai(text, '')
		
		
	async def _do_http_request(self, url, data):
		headers = {
			"Authorization": f"Bearer {os.getenv('API_TOKEN')}",
			"Content-Type": "application/json"
		}
		async with aiohttp.ClientSession() as session:
			async with session.post(url, headers=headers, json=data) as response:
				j = await response.json()
				if "id" in j and "error" in j["id"]:
					raise Exception(json.dumps(j))
				return j
	
	async def open_ai(self, text, system):
		data = {
			"model": "gpt-4.1",
			"max_tokens": 10000,
			"messages": [
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
		res = await self._do_http_request(os.getenv('API_URL'), data)
		return res['choices'][0]['message']['content']
