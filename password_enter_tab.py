import tkinter as tk

def create_password_entry(parent, widgets, textvariable=None):
    placeholder = "Enter your password"
    if textvariable is None:
        textvariable = tk.StringVar()
    password_entry = tk.Entry(
        parent, width=30, font=("Segoe UI", 16, "bold"),
        foreground="grey", justify="center", textvariable=textvariable
    )
    if not textvariable.get():
        password_entry.insert(0, placeholder)
    # Do NOT pack here! Let main.py handle packing order.
    widgets.append(password_entry)

    def on_entry_click(event):
        if password_entry.get() == placeholder:
            password_entry.delete(0, tk.END)
            password_entry.config(foreground="black")

    def on_focusout(event):
        if not password_entry.get():
            password_entry.insert(0, placeholder)
            password_entry.config(foreground="grey", show="")

    password_entry.bind("<FocusIn>", on_entry_click)
    password_entry.bind("<FocusOut>", on_focusout)
    return password_entry