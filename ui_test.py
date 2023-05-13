import pygame
import pygame_gui


class UI:
	def __init__(self, screen_w, screen_h):
		self.manager = pygame_gui.UIManager((screen_w, screen_h))

		# Button to start the scraper
		rect_button_start = pygame.Rect(0, 0, 150, 50)
		self.button_start = pygame_gui.elements.UIButton(
			relative_rect=rect_button_start,
			text="Start chat",
			manager=self.manager
		)

		# Button to stop the scraper
		rect_button_stop = pygame.Rect(0, 50, 150, 50)
		self.button_stop = pygame_gui.elements.UIButton(
			relative_rect=rect_button_stop,
			text="Stop chat",
			manager=self.manager
		)

		# Button to reload the scraper
		rect_button_reload = pygame.Rect(0, 100, 150, 50)
		self.button_reload = pygame_gui.elements.UIButton(
			relative_rect=rect_button_reload,
			text="Reload chat",
			manager=self.manager
		)
