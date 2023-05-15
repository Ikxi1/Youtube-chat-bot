# Always write YouTube as Youtube
# Never fucking write YouTube

import pygame
import pygame_gui
import time
from ui_test import UI
from url_test import get_youtube_id
from chat_test import Chat

pygame.init()


class Program:
	def __init__(self):
		# Prepare normal window
		self.screen_width = 1000  # Screen width in pixels
		self.screen_height = 1000  # Screen height in pixels
		self.screen = pygame.display.set_mode(
			(self.screen_width, self.screen_height),
			pygame.RESIZABLE
		)
		pygame.display.set_caption("Youtube Chatbot by Ikxi")

		self.running = True
		self.clock = pygame.time.Clock()
		self.framerate = 30

		self.chat_running = False

		self.stream_id = ''
		self.valid_url = False

	def run(self):
		print("program running")
		while self.running:
			time_delta = self.clock.tick(self.framerate) / 1000.0

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.chat_stop()
					self.running = False
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.chat_stop()
						self.running = False
					if event.key == pygame.K_g and not self.chat_running:
						self.chat_run()

				# Trying to start the script after stopping it crashes
				elif event.type == pygame_gui.UI_BUTTON_PRESSED:
					if event.ui_element == ui.button_start and not self.chat_running:
						self.chat_run()
					elif event.ui_element == ui.button_stop and self.chat_running:
						self.chat_stop()
					elif event.ui_element == ui.button_reload and self.chat_running:
						self.chat_reload()

				ui.manager.process_events(event)

			if self.chat_running:
				self.chat.run()

			self.screen.fill((0, 0, 0))
			ui.manager.update(time_delta)
			ui.manager.draw_ui(self.screen)
			pygame.display.update()

	def chat_run(self):
		url = ui.textfield_url.get_text()
		self.valid_url, self.stream_id = get_youtube_id(url)
		if self.valid_url:
			ui.label_validurl.set_text("Valid URL")
			self.chat = Chat(self.stream_id)
			self.chat_running = True
		else:
			ui.label_validurl.set_text("Invalid URL")

	def chat_stop(self):
		self.chat_running = False
		self.chat.driver.quit()

	def chat_reload(self):
		self.chat_stop()
		print("Reloading chat")
		time.sleep(1)
		print("3")
		time.sleep(1)
		print("2")
		time.sleep(1)
		print("1")
		self.chat_run()
		print("Chat reloaded")


# Initiate and execute classes
program = Program()
print("program initiated")
ui = UI(program.screen_width, program.screen_height)
print("ui initiated")
program.run()
# Quit the pygame
pygame.quit()
