from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import asyncio
import random

from src.command.router.hot_site.prompt import start, close, close_voice


driver = None

def _start_hotsite():
    global driver
    options = Options()
    options.add_argument('--start-maximized')
    try:
        driver = webdriver.Firefox(options=options)
        driver.get("https://sex-studentki.city/hq-porn/trending")
    except Exception as e:
        print("Ошибка запуска браузера:", e)

def _close_driver():
    global driver
    if driver is not None:
        try:
            driver.quit()
        except Exception:
            pass
        driver = None

async def handle(text, context):
    global driver
    # Если пришла команда закрытия
    if any(i in text.lower() for i in close):
        if driver is not None:
            _close_driver()
            await context.VOICE.voice_generate(random.choice(close_voice['close']))
            return

    # Оповещение о запуске
    word = random.choice(start['hot_site'])
    await context.VOICE.voice_generate(word)
    res = await context.VOICE.response(2, True)

    # Проверка на фразы согласия (одна подстрока вхождения достаточна)
    resp_text = res.lower() if res else ""
    trigger_words = ["подтверждаю", "подтверждаю запуск", "запуск", "запустить"]

    if any(word in resp_text for word in trigger_words):
        await context.VOICE.voice_generate(random.choice(start['start']))
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _start_hotsite)
    else:
        await context.VOICE.voice_generate(random.choice(start['none_start']))