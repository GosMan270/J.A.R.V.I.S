"""
Запрос к ИИ
"""
import aiohttp
import json
import os
from dotenv import load_dotenv




dotenv_patch = os.path.join(os.path.dirname(__file__), 'run', 'config.env')
load_dotenv(dotenv_patch)


class Ai:
    def __init__(self):
        pass


    async def open_ai(self, text, system):
        api_url = os.getenv('API_URL')
        api_token = os.getenv('API_KEY')

        print("API_URL:", api_url)
        print("API_TOKEN:", api_token[:6] + '...')

        data = {
            "model": "gpt-4o",
            "max_tokens": 10000,
            "messages": [
                {"role": "user", "content": text},
                {"role": "system", "content": system}
            ]
        }
        res = await self._do_http_request(api_url, api_token, data)
        return res['choices'][0]['message']['content']


    async def _do_http_request(self, url, token, data):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=data) as response:
                j = await response.json()
                if "id" in j and "error" in j["id"]:
                    raise Exception(json.dumps(j))
                return j


async def handle(text, system):
    AI = Ai()
    res = await AI.open_ai(text, system)
    return res