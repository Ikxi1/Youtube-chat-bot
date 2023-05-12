from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get('https://www.youtube.com/live_chat?v=x2RK5dYMSv4')
wait = WebDriverWait(driver, 10)

while True:
    messages = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'yt-live-chat-text-message-renderer')))
    for message in messages:
        author_name = message.find_element(By.ID, 'author-name').text
        message_text = message.find_element(By.ID, 'message').text
        print(f'{author_name}: {message_text}')
    time.sleep(1)
