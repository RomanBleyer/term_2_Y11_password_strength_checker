import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

def copy_to_clipboard_button(parent, password_entry, widgets):
    image_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "copy_to_clipboard.png")
    copy_img = Image.open(image_path).resize((32, 32))
    copy_to_clipboard_image = ImageTk.PhotoImage(copy_img)

    def copy_to_clipboard():
        password = password_entry.get()
        parent.clipboard_clear()
        parent.clipboard_append(password)

    copy_btn = ttk.Button(parent, image=copy_to_clipboard_image, command=copy_to_clipboard)
    copy_btn.image = copy_to_clipboard_image  # Prevent image garbage collection
    widgets.append(copy_btn)
    return copy_btn

