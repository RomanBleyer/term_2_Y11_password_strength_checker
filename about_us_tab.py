from PIL import Image, ImageTk
import tkinter as tk
import os

def about_us_button(master, widgets, go_to_about_callback):
    # Load the image using an absolute path
    image_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "about_us.png")
    img = Image.open(image_path)
    img = img.resize((30, 30), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)
    
    btn = tk.Button(master, image=photo, command=go_to_about_callback, borderwidth=0)
    btn.image = photo  # Keep a reference to avoid garbage collection
    btn.place(x=0, y=0, width=40, height=40)
    widgets.append(btn)
    return btn