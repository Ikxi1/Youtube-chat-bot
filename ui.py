import pygame
import pygame_gui


class UI:
	def __init__(self, screen_w, screen_h):
		self.manager = pygame_gui.UIManager((screen_w, screen_h))

		# Button to start the scraper
		rect_button_start = pygame.Rect(20, 20, 150, 50)
		self.button_start = pygame_gui.elements.UIButton(
			relative_rect=rect_button_start,
			text="Start chat",
			manager=self.manager
		)

		# Button to reload the scraper
		rect_button_reload = pygame.Rect(20, 90, 150, 50)
		self.button_reload = pygame_gui.elements.UIButton(
			relative_rect=rect_button_reload,
			text="Reload chat",
			manager=self.manager
		)

		# Button to stop the scraper
		rect_button_stop = pygame.Rect(20, 160, 150, 50)
		self.button_stop = pygame_gui.elements.UIButton(
			relative_rect=rect_button_stop,
			text="Stop chat",
			manager=self.manager
		)

		# Label to explain text field
		rect_label_url = pygame.Rect(20, 230, 600, 50)
		self.label_url = pygame_gui.elements.UITextBox(
			relative_rect=rect_label_url,
			html_text="Copy your stream URL here<br>Example: https://www.youtube.com/watch?v=EX75DyJvE8g",
			manager=self.manager,
			wrap_to_height=True
		)

		# Text field for the Youtube link
		rect_textfield_url = pygame.Rect(20, 300, 600, 50)
		self.textfield_url = pygame_gui.elements.UITextEntryLine(
			relative_rect=rect_textfield_url,
			manager=self.manager
		)

		# Text field for, if there is a URL and if it's valid
		rect_label_validurl = pygame.Rect(620, 300, 200, 50)
		self.label_validurl = pygame_gui.elements.UILabel(
			relative_rect=rect_label_validurl,
			text="No URL detected",
			manager=self.manager
		)
