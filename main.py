# Always write YouTube as Youtube
# Never fucking write YouTube

import tkinter as tk
import tkinter.font as tkfont
import time
import threading
from PIL import Image, ImageTk
from chat import Chat
from url import get_youtube_id


# https://www.phind.com/search?cache=a5745e4a-a263-4cfd-baea-d66637c5174c
class Program(tk.Tk):
	def __init__(self):
		super().__init__()

		self.geometry("1000x500")

		self.valid_url = False
		self.chat_running = False

		font = tkfont.Font(family='Circular Std', size=30)
		self.option_add("*Font", font)

		button_image = Image.open("assets/button_start_chat.png")
		button_new_size = (button_image.width // 2, button_image.height // 2)
		button_image_resized = button_image.resize(button_new_size)
		self.button_image = ImageTk.PhotoImage(button_image_resized)

		self.label_url = tk.Label(self, text='Copy your stream URL here\nExample: https://www.youtube.com/watch?v=EX75DyJvE8g')
		self.label_url.pack()

		self.entry_url = tk.Entry(self)
		self.entry_url.pack()

		self.label_valid_url = tk.Label(self, text='')
		self.label_valid_url.pack()

		self.button_start = tk.Button(
			self,
			command=self.chat_init,
			image=self.button_image
		)
		self.button_start["bg"] = "white"
		self.button_start["border"] = "0"
		self.button_start.pack()

		self.button_reload = tk.Button(self, text='Reload Chat', command=self.chat_reload)
		self.button_reload.pack()

		self.button_stop = tk.Button(self, text='Stop Chat', command=self.chat_stop)
		self.button_stop.pack()

		self.button_quit = tk.Button(self, text='Quit Program', command=self.stop_program)
		self.button_quit.pack()

	def chat_init(self):
		self.valid_url, stream_id = get_youtube_id(self.entry_url.get())
		if self.valid_url:
			self.label_valid_url.config(text="Valid URL")
			self.chat = Chat(stream_id)
			self.loop_thread = threading.Thread(target=self.chat.run)
			self.chat.running = True
			self.chat_run()
		else:
			self.label_valid_url.config(text="Invalid URL")

	def chat_run(self):
		self.loop_thread.start()

	def chat_stop(self):
		try:
			if self.chat.running:
				self.chat.running = False
		except:
			pass

	def chat_reload(self):
		if self.chat.running:
			self.chat_stop()
			print("Chat reloading")
			time.sleep(1)
			print("...")
			time.sleep(1)
			print("...")
			self.chat_init()
			print("Chat reloaded")

	def stop_program(self):
		self.chat_stop()

		self.quit()


root = Program()
print("program initiated")
# mainloop is a tkinter method, runs application's main event loop
root.mainloop()
