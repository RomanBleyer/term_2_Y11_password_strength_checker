import tkinter as tk

def back_to_main_menu_button(master, widgets, go_to_main_menu_callback):
    back_btn = tk.Button(master, text="Back", command=go_to_main_menu_callback)
    # Do NOT pack here! Let main.py handle packing order.
    widgets.append(back_btn)
    return back_btn