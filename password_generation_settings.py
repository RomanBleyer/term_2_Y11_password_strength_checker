import tkinter as tk

use_capital_letters = True
use_special_characters = True
use_numbers = True
copy_after_generation = True
check_strength_after_generation = True

def create_password_generation_settings(master, widgets, state):
    # state should be a dict with the 5 boolean values, e.g.:
    # state = {
    #     "use_capital_letters": True,
    #     "use_special_characters": True,
    #     "use_numbers": True,
    #     "copy_after_generation": True,
    #     "check_strength_after_generation": True
    # }

    def toggle(key, button):
        state[key] = not state[key]
        button.config(text=f"{labels[key]}: {state[key]}")

    labels = {
        "use_capital_letters": "Use Capital Letters",
        "use_special_characters": "Use Special Characters",
        "use_numbers": "Use Numbers",
        "copy_after_generation": "Copy After Generation",
        "check_strength_after_generation": "Check Strength After Generation"
    }

    buttons = {}
    for idx, key in enumerate(labels):
        btn = tk.Button(
            master,
            text=f"{labels[key]}: {state[key]}",
            command=lambda k=key, b=None: None  # Placeholder, will set below
        )
        # Set the correct command after creation to avoid late binding issue
        btn.config(command=lambda k=key, b=btn: toggle(k, b))
        btn.pack(pady=(5, 0))
        widgets.append(btn)
        buttons[key] = btn

    return buttons