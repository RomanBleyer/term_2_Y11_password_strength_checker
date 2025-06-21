import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

def hide_unhide_password_button(parent, password_entry, widgets, show_password_state):
    # Use correct filenames
    eye_open_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "eye_open.png")
    eye_closed_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "eye_closed.png")
    eye_open = Image.open(eye_open_path).resize((32, 32))
    eye_closed = Image.open(eye_closed_path).resize((32, 32))
    eye_open_image = ImageTk.PhotoImage(eye_open)
    eye_closed_image = ImageTk.PhotoImage(eye_closed)

    def toggle_password():
        show_password_state[0] = not show_password_state[0]
        if show_password_state[0]:
            password_entry.config(show="")
            toggle_btn.config(image=eye_open_image)
        else:
            password_entry.config(show="•")
            toggle_btn.config(image=eye_closed_image)

    # Set initial state based on show_password_state[0]
    if show_password_state[0]:
        password_entry.config(show="")
        initial_image = eye_open_image
    else:
        password_entry.config(show="•")
        initial_image = eye_closed_image

    toggle_btn = ttk.Button(parent, image=initial_image, command=toggle_password)
    toggle_btn.image_open = eye_open_image
    toggle_btn.image_closed = eye_closed_image
    # Do NOT pack here! Let main.py handle packing order.
    widgets.append(toggle_btn)
    return toggle_btn