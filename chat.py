from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import re
import time
from w_r_files import Files
import bot_login
from chat_ui import ChatUI


class Chat:
	def __init__(self, stream_id):
		self.missed_name = 0
		self.raid = 0
		self.running = True

		# Prepare and open the browser window
		options = webdriver.ChromeOptions()
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
		options.add_argument("--mute-audio")

		service = Service("chromedriver.exe")
		self.driver = webdriver.Chrome(service=service, options=options)

		# Youtube link
		self.link = "https://www.youtube.com/live_chat?v=" + stream_id

		# Get the latest list of messages
		self.driver.get(self.link)

		# Files being initiated
		self.files = Files()

		self.timestamp_button = self.driver.find_element(By.XPATH, '//*[@id="live-chat-header-context-menu"]')
		self.timestamp_button.click()
		time.sleep(1)
		self.timestamp_button = self.driver.find_element(By.XPATH, "/html/body/yt-live-chat-app/tp-yt-iron-dropdown/div/ytd-menu-popup-renderer/tp-yt-paper-listbox/ytd-menu-service-item-renderer[2]/tp-yt-paper-item")
		self.timestamp_button.click()

		bot_login.click_login(self.driver, stream_id)

		self.chat_ui = ChatUI()

	def run(self):
		message_id = ''
		while self.running:
			message_list = self.driver.find_elements(
				By.CSS_SELECTOR,
				'yt-live-chat-text-message-renderer'
			)
			for message in message_list:
				# Get the ID of the current message
				# Just 1 ID, not a set of IDs
				# Just a string
				try:
					message_id = message.get_attribute('id')
				except:
					pass
				# Check if the message has already been processed
				if message_id not in self.files.message_ids:
					try:
						timestamp = message.find_element(By.CSS_SELECTOR, '#timestamp').text
					except:
						timestamp = ''

					# Find username
					try:
						username = message.find_element(By.CSS_SELECTOR, '#author-name').text
					except:
						username = 'none'

					if username == "Ikxi_Bot":
						self.files.write_message_ids(message_id)
						break

					# Find message and emotes
					try:
						try:
							# Try to find the text of the message
							msg_elem = message.find_element(
								By.CSS_SELECTOR,
								'#message #message-text yt-formatted-string'
							)
							msg = msg_elem.text

							# Find all emotes in the message
							emotes = message.find_elements(By.CSS_SELECTOR, '#message img')
							# Loop through all the emotes in reverse order
							for emote in emotes[::-1]:
								alt_text = emote.get_attribute('alt')
								# Find the index of the emote in the original message text
								emote_index = msg_elem.get_attribute('innerHTML').index(emote.get_attribute('outerHTML'))
								# Insert the emote at its original position in the message text
								msg = msg[:emote_index] + ':' + alt_text + ':' + msg[emote_index:]
						except:
							# If the text is not found, use the HTML of the message
							html = message.find_element(By.CSS_SELECTOR, '#message').get_attribute('innerHTML')
							msg = re.sub('<[^<]+?>', '', html)
							# Find all emotes in the message
							emotes = message.find_elements(By.CSS_SELECTOR, '#message img')
							# Loop through all the emotes in reverse order
							for emote in emotes[::-1]:
								alt_text = emote.get_attribute('alt')
								# Find the index of the emote in the original message text
								emote_index = html.index(emote.get_attribute('outerHTML'))
								# Insert the emote at its original position in the message text
								msg = msg[:emote_index] + ':' + alt_text + ':' + msg[emote_index:]
					except:
						msg = ''

					# Name substitutions
					if username in self.files.exchange_names:
						username = self.files.exchange_names.get(username)

					# If the message contains a blocked word, skip it
					if any(word in msg.lower() for word in self.files.blocked_words):
						msg = "<filtered>"

					# Check for raids
					if "raid" in msg and message_id not in self.files.raid_ids:
						self.raid += 1
						self.files.write_raid_ids(message_id)

					# Add all parts to full message
					self.full_message = timestamp + ' : ' + username + ' : ' + msg
					# Print the message
					self.chat_ui.display_message(self.full_message)
					# print(self.full_message)

					# Write number of times a name was missed
					if self.missed_name > 0:
						print("Missed a name:", self.missed_name, "times.")

					# Add full message to file
					self.files.write_messages(self.full_message)

					# Check if message is a command
					if msg in self.files.commands:
						text = self.files.commands.get(msg)
						text_box = self.driver.find_element(By.XPATH, '//*[@id="input"]')
						text_box.send_keys(text + Keys.RETURN)

					# Print if a raid is happening
					if self.raid >= 5:
						print("THERE IS A RAID HAPPENING!!!")
						self.raid = 0

					# Print if someone tells me to sleep
					if "you should go to sleep" in msg or "You should go to sleep" in msg:
						print("I won't go to sleep")

					self.missed_name = 0

					# Add the message ID to the set of processed messages
					# and write it to the file
					self.files.write_message_ids(message_id)
		self.driver.quit()

	def stop(self):
		self.running = False
