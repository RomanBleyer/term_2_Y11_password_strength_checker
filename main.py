import tkinter as tk
from tkinter import ttk

# File function imports
from password_enter_tab import create_password_entry
from copy_to_clipboard_button import copy_to_clipboard_button
from hide_unhide_password import hide_unhide_password_button
from password_generator_settings_button import password_generator_settings_button
from back_to_main_menu_button import back_to_main_menu_button
from password_generation_settings import create_password_generation_settings

class PasswordStrengthChecker:
    def __init__(self, master):
        self.master = master

        self.master.resizable(False, False)
        self.master.geometry(f"500x200+{self.master.winfo_screenwidth()-510}+{self.master.winfo_screenheight()-280}")

        # Track which page we're on
        self.what_page_am_i_on = getattr(self, "what_page_am_i_on", "main_menu")

        # Settings state dict (persistent)
        self.settings_state = {
            "use_capital_letters": True,
            "use_special_characters": True,
            "use_numbers": True,
            "copy_after_generation": True,
            "check_strength_after_generation": True
        }

        if self.what_page_am_i_on == "main_menu":
            widgets = []
            # Title
            title = ttk.Label(self.master, text="Password Strength Checker", font=("Segoe UI", 18, "bold"))
            title.place(x=100, y=10)
            widgets.append(title)

            # Entry row frame
            entry_frame = tk.Frame(self.master)
            entry_frame.place(x=40, y=60, width=420, height=40)
            widgets.append(entry_frame)

            # Entry row widgets
            copy_btn = copy_to_clipboard_button(entry_frame, None, widgets)
            password_entry = create_password_entry(entry_frame, widgets)
            show_password_state = [True]
            eye_btn = hide_unhide_password_button(entry_frame, password_entry, widgets, show_password_state)

            # Place entry row widgets
            copy_btn.place(x=0, y=0, width=40, height=40)
            password_entry.place(x=45, y=0, width=280, height=40)
            eye_btn.place(x=330, y=0, width=40, height=40)

            # Settings button below entry row
            settings_frame = tk.Frame(self.master)
            settings_frame.place(x=200, y=110, width=100, height=40)
            widgets.append(settings_frame)
            def go_to_settings():
                for widget in widgets:
                    widget.destroy()
                widgets.clear()
                self.what_page_am_i_on = "password_generator_settings_menu"
                self.__init__(self.master)
            settings_btn = password_generator_settings_button(settings_frame, widgets, go_to_settings)
            settings_btn.place(x=0, y=0, width=40, height=40)

        elif self.what_page_am_i_on == "password_generator_settings_menu":
            settings_widgets = []

            # 5 toggle buttons for settings (no title)
            buttons = create_password_generation_settings(
                self.master,
                settings_widgets,
                self.settings_state
            )
            y_offset = 5  # Start closer to the top
            for idx, btn in enumerate(buttons.values()):
                btn.place(x=100, y=y_offset + idx * 28, width=300, height=25)

            # Small print at the bottom
            small_print = ttk.Label(
                self.master,
                text="press enter to return to the main menu",
                font=("Segoe UI", 8, "italic")
            )
            small_print.place(x=140, y=y_offset + 5 * 28 + 10)
            settings_widgets.append(small_print)

            # Bind Enter key to return to main menu and save settings
            def on_enter(event):
                # If your toggle buttons update self.settings_state directly, nothing else is needed here.
                for widget in settings_widgets:
                    widget.destroy()
                settings_widgets.clear()
                self.what_page_am_i_on = "main_menu"
                self.__init__(self.master)
            if self.what_page_am_i_on == "password_generator_settings_menu":
                self.master.bind('<Return>', on_enter)

        elif self.what_page_am_i_on == "about_me_and_help_menu":
            # all displays for about me and help menu here
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()