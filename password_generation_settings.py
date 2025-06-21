import tkinter as tk

def create_password_generation_settings(master, widgets, state):
    labels = {
        "use_capital_letters": "Use Capital Letters",
        "use_special_characters": "Use Special Characters",
        "use_numbers": "Use Numbers",
        "copy_after_generation": "Copy After Generation",
        "check_strength_after_generation": "Check Strength After Generation"
    }
    buttons = {}

    def make_toggle(key):
        def toggle():
            state[key] = not state[key]
            btn.config(text=f"{labels[key]}: {state[key]}")
        btn = tk.Button(
            master,
            text=f"{labels[key]}: {state[key]}",
            command=toggle,
            font=("Segoe UI", 10),
            width=30
        )
        widgets.append(btn)
        buttons[key] = btn
        return btn

    for key in labels:
        make_toggle(key)

    return buttons