import tkinter as tk
from tkinter import ttk
import random
import string

def generate_password(settings, length):
    chars = string.ascii_lowercase
    if settings.get("use_capital_letters", True):
        chars += string.ascii_uppercase
    if settings.get("use_numbers", True):
        chars += string.digits
    if settings.get("use_special_characters", True):
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>/?"
    if not chars:
        chars = string.ascii_letters  # fallback

    return ''.join(random.choice(chars) for _ in range(length))

class PasswordGeneratorUI:
    def __init__(self, master, settings_state):
        self.master = master
        self.settings_state = settings_state
        self.widgets = []

        # Label
        label = ttk.Label(self.master, text="Maximum of 16 characters", font=("Segoe UI", 10, "bold"))
        label.pack(pady=(10, 0))
        self.widgets.append(label)

        # Number Entry (Password Length)
        def validate_number(P):
            if P == "":
                return True
            if P.isdigit():
                value = int(P)
                return 1 <= value <= 16
            return False

        vcmd = (self.master.register(validate_number), "%P")
        self.number_var = tk.StringVar(value="12")
        self.number_entry = tk.Entry(
            self.master,
            textvariable=self.number_var,
            validate="key",
            validatecommand=vcmd,
            width=5,
            font=("TkDefaultFont", 10, "bold"),
            justify="center"
        )
        self.number_entry.pack(pady=(5, 0))
        self.widgets.append(self.number_entry)

        # Password Entry (blocks spaces)
        def block_space(event):
            if event.char == " ":
                return "break"

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            self.master,
            textvariable=self.password_var,
            font=("TkDefaultFont", 12, "bold"),
            justify="center",
            width=30
        )
        self.password_entry.pack(pady=(5, 0))
        self.password_entry.bind("<Key>", block_space)
        self.widgets.append(self.password_entry)

        # Generate Button
        def on_generate():
            try:
                length = int(self.length_var.get())
            except ValueError:
                length = 12
            pwd = generate_password(self.settings_state, length)
            self.password_var.set(pwd)

        gen_btn = tk.Button(self.master, text="Generate Password", font=("Segoe UI", 12, "bold"), command=on_generate)
        gen_btn.pack(pady=(10, 0))
        self.widgets.append(gen_btn)

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    settings_state = {
        "use_capital_letters": True,
        "use_special_characters": True,
        "use_numbers": True,
        "copy_after_generation": True,
        "check_strength_after_generation": True
    }
    PasswordGeneratorUI(root, settings_state)
    root.mainloop()

