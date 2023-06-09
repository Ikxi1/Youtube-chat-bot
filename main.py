# Always write YouTube as Youtube
# Never fucking write YouTube

import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk
import time
import threading
from PIL import Image, ImageTk
from chat import Chat
from url import get_youtube_id


class Program(ctk.CTk):
	def __init__(self):
		super().__init__()

		# self.geometry("1000x500")

		self.valid_url = False
		self.chat_running = False

		font1 = ctk.CTkFont(family='Roboto', size=30, weight='bold')
		font2 = ctk.CTkFont(family='Roboto', size=24)

		self.frame = ctk.CTkFrame(self)
		self.frame.pack(padx=20, pady=20, expand=True, fill="both")

		self.label_url = ctk.CTkLabel(self.frame, font=font1, text='Stream URL:')
		self.label_url.pack(padx=2, pady=2)

		self.entry_url = ctk.CTkEntry(self.frame, width=700, font=font1, placeholder_text='https://www.youtube.com/watch?v=***********')
		self.entry_url.pack(padx=2, pady=2)

		button_width = 275
		button_height = 55

		self.button_start = ctk.CTkButton(
			self.frame,
			text='Start Chat',
			command=self.chat_init,
			font=font1,
			width=button_width,
			height=button_height
		)
		self.button_start.pack(padx=2, pady=2)

		self.button_reload = ctk.CTkButton(
			self.frame,
			text='Reload Chat',
			command=self.chat_reload,
			font=font1,
			width=button_width,
			height=button_height
		)
		self.button_reload.pack(padx=2, pady=2)

		self.button_stop = ctk.CTkButton(
			self.frame,
			text='Stop Chat',
			command=self.chat_stop,
			font=font1,
			width=button_width,
			height=button_height
		)
		self.button_stop.pack(padx=2, pady=2)

		self.button_quit = ctk.CTkButton(
			self.frame,
			text='Quit Program',
			command=self.stop_program,
			font=font1,
			width=button_width,
			height=button_height
		)
		self.button_quit.pack(padx=2, pady=2)

		# self.label_valid_url = tk.Label(self, text='')
		# self.label_valid_url.pack()

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
