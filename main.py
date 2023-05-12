# Always write YouTube as Youtube
# Never fucking write YouTube

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import re
import gc
import pygame
import pygame_gui
from w_r_files import Files
from ui import UI


class Program:
	def __init__(self):
		# Prepare normal window
		pygame.init()
		screen_width = 1000  # Screen width in pixels
		screen_height = 1000  # Screen height in pixels
		screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
		pygame.display.set_caption("Youtube Chatbot by Ikxi")

		self.running = True
		self.clock = pygame.time.Clock
		self.framerate = 30

		self.missed_name = 0
		self.raid = 0

		# Prepare browser window
		options = webdriver.ChromeOptions()
		options.add_experimental_option('excludeSwitches', ['enable-logging'])

		service = Service("chromedriver.exe")
		self.driver = webdriver.Chrome(service=service, options=options)

		# Youtube link
		stream_id = "EX75DyJvE8g"
		self.link = "https://www.youtube.com/live_chat?v=" + stream_id

	def run_main(self):
		while self.running:
			# time_delta = self.clock.tick(self.framerate) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.running = False
					if event.key == pygame.K_g:
						self.run_second()

			pygame.display.update()
			gc.collect()

	def run_second(self):
		# Get the latest list of messages
		self.driver.get(self.link)
		message_list = self.driver.find_elements(By.CSS_SELECTOR, 'yt-live-chat-text-message-renderer')
		for message in message_list:
			# Get the ID of the current message
			# Just 1 ID, not a set of IDs
			# Just a string
			message_id = message.get_attribute('id')
			# Check if the message has already been processed
			if message_id not in files.message_ids:
				# The timestamps don't work when you reload the script, they only then show the current time, not when the message was sent
				timestamp = datetime.now().strftime("%H:%M:%S")

				# Find username
				username = message.find_element(By.CSS_SELECTOR, '#author-name').text
				if username == "":
					self.missed_name += 1
					break

				# Find message and emotes
				try:
					# Try to find the text of the message
					msg_elem = message.find_element(By.CSS_SELECTOR, '#message #message-text yt-formatted-string')
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

				# Name substitutions
				if username in files.exchange_names:
					username = files.exchange_names.get(username)

				# If the message contains a blocked word, skip it
				if any(word in msg.lower() for word in files.blocked_words):
					msg = "<filtered>"

				# Check if message is a command
				if msg in files.commands:
					print("This is a command\nCommands are not implemented yet")

				# Check for raids
				if "raid" in msg and message_id not in files.raid_ids:
					self.raid += 1
					files.write_raid_ids(message_id)

				# Add all parts to full message
				full_message = timestamp + ' : ' + username + ' : ' + msg
				# Print the message
				print(full_message)

				# Write number of times a name was missed
				if self.missed_name > 0:
					print("Missed a name:", self.missed_name, "times.")

				# Add full message to file
				files.write_messages(full_message)

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
				files.write_message_ids(message_id)


# Initiate and execute classes
files = Files()
ui = UI()
program = Program()
program.run_main()
# Quit the pygame
pygame.quit()
# Close the browser
program.driver.quit()
