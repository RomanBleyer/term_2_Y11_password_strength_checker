import tkinter as tk

def create_password_entry(parent, widgets):
    placeholder = "Enter your password"
    password_entry = tk.Entry(
        parent, width=30, font=("Segoe UI", 16, "bold"),
        foreground="grey", justify="center"
    )
    password_entry.insert(0, placeholder)
    password_entry.pack(side="right", padx=(5, 0))  # Entry on the right
    widgets.append(password_entry)

    def on_entry_click(event):
        if password_entry.get() == placeholder:
            password_entry.delete(0, tk.END)

    def on_focusout(event):
        if not password_entry.get():
            password_entry.insert(0, placeholder)
            password_entry.config(foreground="grey", show="")

    password_entry.bind("<FocusIn>", on_entry_click)
    password_entry.bind("<FocusOut>", on_focusout)
    return password_entry