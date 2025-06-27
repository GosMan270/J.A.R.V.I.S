import aiohttp
import json

from src.data.run.config import config


class Ai:
	def __init__(self):
		pass
	
	
	async def handle(text, context):
		if text and "закрыть протокол наслаждение" or "закрыть протокол наслаждение" or "закрыть протокол наслаждения" or "закрыть протокол наслажденье" or "закрыть протокол наслаждения" or "закрыть протокол наслаждений" or "завершить протокол наслаждение" or "завершить протокол наслаждение" or "закрыть протокол наслаждения" or "закрыть протокол наслажденье" or "закрыть протокол наслаждения" or "закрыть протокол наслаждений" in text.lower():
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
		res = await self._do_http_request(config["api_url"], data)
		return res['choices'][0]['message']['content']
