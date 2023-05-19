import tkinter as tk
import tkinter.font as tkfont


class ChatUI(tk.Toplevel):
	def __init__(self):
		super().__init__()

		self.geometry("500x1000")

		font = tkfont.Font(family='Circular Std', size=10)
		self.option_add("*Font", font)

		self.message1_text = tk.StringVar()
		self.message2_text = tk.StringVar()
		self.message3_text = tk.StringVar()

		self.label_message1 = tk.Label(self, textvariable=self.message1_text)
		self.label_message1.pack()

		self.label_message2 = tk.Label(self, textvariable=self.message2_text)
		self.label_message2.pack()

		self.label_message3 = tk.Label(self, textvariable=self.message3_text)
		self.label_message3.pack()

	def display_message(self, full_message):

		message1 = self.message1_text.get()
		message2 = self.message2_text.get()

		self.message1_text.set(full_message)
		self.message2_text.set(message1)
		self.message3_text.set(message2)
