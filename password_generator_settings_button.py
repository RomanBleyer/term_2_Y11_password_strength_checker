import tkinter as tk
from PIL import Image, ImageTk
import os

def password_generator_settings_button(master, widgets, go_to_settings_callback):
    image_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "settings_gear.png")
    settings_img = Image.open(image_path).resize((15, 15))
    settings_image = ImageTk.PhotoImage(settings_img)

    settings_button = tk.Button(
        master,
        image=settings_image,
        command=go_to_settings_callback,
        borderwidth=0
    )
    settings_button.image = settings_image  # Prevent garbage collection
    # Do NOT pack here! Let main.py handle packing order.
    widgets.append(settings_button)
    return settings_button


