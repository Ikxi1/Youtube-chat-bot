import tkinter as tk
import tkinter.font as tkfont

num_labels = 40


class ChatUI(tk.Toplevel):
	def __init__(self):
		super().__init__()

		self.geometry("500x1000")

		font = tkfont.Font(family='Circular Std', size=10)
		self.option_add("*Font", font)

		self.labels = []
		self.label_texts = []

		for i in range(num_labels):
			label_text = tk.StringVar()
			self.label_texts.append(label_text)

			label = tk.Label(self, textvariable=label_text)
			label.pack()
			self.labels.append(label)

	def display_message(self, full_message):
		# Shift the messages down by one position
		for i in reversed(range(1, num_labels)):
			self.label_texts[i].set(self.label_texts[i - 1].get())

		# Set the full_message to the first label
		self.label_texts[0].set(full_message)
