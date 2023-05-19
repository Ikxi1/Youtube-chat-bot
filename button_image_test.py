import tkinter as tk
from PIL import Image, ImageTk

def on_button_click():
    print("Button clicked")

root = tk.Tk()

# Open the image file
image = Image.open("assets/button_2.png")

# Calculate the new size of the image
new_size = (image.width // 2, image.height // 2)

# Resize the image
resized_image = image.resize(new_size)

# Convert the resized image to a PhotoImage object
photo_image = ImageTk.PhotoImage(resized_image)

# Create a button with the resized image
button = tk.Button(root, image=photo_image, command=on_button_click)
button.pack()

root.mainloop()
