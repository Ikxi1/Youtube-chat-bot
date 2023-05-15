from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bot_login_keys
import time


def click_login(driver, stream_id):
	login_button = driver.find_element(By.XPATH, '/html/body/yt-live-chat-app/div/yt-live-chat-renderer/iron-pages/div/div[1]/iron-pages/div[1]/yt-live-chat-message-input-renderer/div[2]/yt-live-chat-message-renderer/div[2]')
	login_button.click()
	login_textfield_email = driver.find_element(By.XPATH, '//*[@id="identifierId"]')
	login_textfield_email.send_keys(bot_login_keys.email + Keys.RETURN)
	time.sleep(5)
	login_textfield_pw = driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
	login_textfield_pw.send_keys(bot_login_keys.password + Keys.RETURN)
	time.sleep(3)
	driver.get("https://www.youtube.com/live_chat?v=" + stream_id)
	time.sleep(2)
