import tkinter as tk
from tkinter import ttk

def show_about_us_window(master, return_to_main_menu_callback):
    widgets = []

    # "About this program" title, centered
    title = ttk.Label(master, text="about this program", font=("Segoe UI", 16, "bold"))
    title.place(relx=0.5, y=40, anchor="center")
    widgets.append(title)

    # Placeholder description, centered
    desc = ttk.Label(master, text="This is a placeholder description", font=("Segoe UI", 12))
    desc.place(relx=0.5, y=80, anchor="center")
    widgets.append(desc)

    # Fine print at the bottom
    fine_print = ttk.Label(master, text="press enter to return to the main menu", font=("Segoe UI", 8, "italic"))
    fine_print.place(relx=0.5, rely=1.0, y=-20, anchor="s")
    widgets.append(fine_print)

    # Bind Enter key to return to main menu
    def on_enter(event):
        for widget in widgets:
            widget.destroy()
        widgets.clear()
        return_to_main_menu_callback()

    master.bind('<Return>', on_enter)
    return