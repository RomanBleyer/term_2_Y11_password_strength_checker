import tkinter as tk

def create_password_entry(master, widgets):
    placeholder = "Enter your password"
    password_entry = tk.Entry(
        master, width=30, font=("Segoe UI", 16, "bold"),
        foreground="grey", justify="center"
    )
    password_entry.insert(0, placeholder)
    password_entry.pack(pady=(0, 5), padx=20)
    widgets.append(password_entry)

    def on_entry_click(event):  # Accept event argument
        if password_entry.get() == placeholder:
            password_entry.delete(0, tk.END)

    def on_focusout(event):  # Accept event argument
        if not password_entry.get():
            password_entry.insert(0, placeholder)
            password_entry.config(foreground="grey", show="")

    password_entry.bind("<FocusIn>", on_entry_click)
    password_entry.bind("<FocusOut>", on_focusout)
    return password_entry