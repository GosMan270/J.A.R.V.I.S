from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import asyncio
import random

from src.command.router.new_day.prompt import start

#ПРИНИМАЕМ ТЕКСТ ОТ VOSK ДАЖЕ ЕСЛИ НЕ НУЖЕН!
async def handle(text, context):
	await context.VOICE.voice_generate(random.choice(start['new_day']))
	await asyncio.sleep(1)
	print(">> Первая реплика проиграна")
	res = await context.VOICE.response(2, True)
	print(">> 2 реплика проиграна")
	
	if res and "да" in res.lower():
		await context.VOICE.voice_generate(random.choice(start['start_music']))
		
		def _start_youtube_playlist():
			options = Options()
			options.add_argument('--start-maximized')
			# путь к вашему профилю Firefox
			profile_path = r"C:\\Users\\user\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\zlob0vsa.default-release"
			options.profile = profile_path
			
			try:
				driver = webdriver.Firefox(options=options)
				driver.get("https://www.youtube.com/watch?v=gEPmA3USJdI&list=PLT54KZJeCRLj8Wjr4fLnzpjFj5_VKPu5J")
				wait = WebDriverWait(driver, 10)
				
				try:
					not_now_btn = wait.until(
						EC.element_to_be_clickable((By.XPATH, "//tp-yt-paper-button[@aria-label='Не сейчас']"))
					)
					not_now_btn.click()
				except Exception:
					pass
				
				try:
					video = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "video")))
					video.click()
				except Exception:
					pass
				
				try:
					play_btn = wait.until(
						EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ytp-play-button"))
					)
					if play_btn.get_attribute('aria-label') in ['Воспроизвести', 'Play']:
						play_btn.click()
				except Exception:
					pass
				
				try:
					body = driver.find_element(By.TAG_NAME, "body")
					body.send_keys("k")
				except Exception:
					pass
			
			except Exception as e:
				print("Ошибка запуска музыки:", e)
		
		loop = asyncio.get_running_loop()
		await loop.run_in_executor(None, _start_youtube_playlist)
	else:
		await context.VOICE.voice_generate(random.choice(start['playlist_cancel']))