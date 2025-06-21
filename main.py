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

        self.master.resizable(False, False) # prevent resizing
        self.master.geometry(f"500x200+{self.master.winfo_screenwidth()-510}+{self.master.winfo_screenheight()-280}") # force window size and position when opened

        # Track which page we're on
        self.what_page_am_i_on = getattr(self, "what_page_am_i_on", "main_menu")

        # Example state dict (should be an attribute of your class for persistence)
        self.settings_state = {
            "use_capital_letters": True,
            "use_special_characters": True,
            "use_numbers": True,
            "copy_after_generation": True,
            "check_strength_after_generation": True
        }

        if self.what_page_am_i_on == "main_menu":
            widgets = []
            title = ttk.Label(self.master, text="Password Strength Checker", font=("Segoe UI", 18, "bold"))
            title.pack(pady=(10, 5))
            widgets.append(title)

            # Create a frame for the entry row
            entry_frame = tk.Frame(self.master)
            entry_frame.pack(pady=(0, 5), padx=20, fill="x", expand=True)
            widgets.append(entry_frame)  # <--- Add this line

            # Create widgets (do NOT pack in their own files)
            copy_btn = copy_to_clipboard_button(entry_frame, None, widgets)
            password_entry = create_password_entry(entry_frame, widgets)
            show_password_state = [True]
            eye_btn = hide_unhide_password_button(entry_frame, password_entry, widgets, show_password_state)

            # Now pack them in the desired order
            copy_btn.pack(side="left", padx=(0, 5))
            password_entry.pack(side="left", padx=(0, 5), fill="x", expand=True)
            eye_btn.pack(side="left", padx=(0, 5))

            def go_to_settings():
                for widget in widgets:
                    widget.destroy()
                widgets.clear()
                self.what_page_am_i_on = "password_generator_settings_menu"
                self.__init__(self.master)  # Re-initialize to load the settings menu

            # Settings button centered below the entry row
            settings_frame = tk.Frame(self.master)
            settings_frame.pack(pady=(10, 0), fill="x", expand=True)
            widgets.append(settings_frame)  # <--- Add this line
            settings_btn = password_generator_settings_button(settings_frame, widgets, go_to_settings)
            settings_btn.pack(anchor="center")

        elif self.what_page_am_i_on == "password_generator_settings_menu":
            settings_widgets = []
            title = ttk.Label(self.master, text="Password Generator Settings", font=("Segoe UI", 18, "bold"))
            title.pack(pady=(10, 5))
            settings_widgets.append(title)

            # Add the three toggle buttons
            buttons = create_password_generation_settings(
                self.master,
                settings_widgets,
                self.settings_state
            )
            for btn in buttons.values():
                btn.pack(pady=(5, 0))

            def go_to_main_menu():
                for widget in settings_widgets:
                    widget.destroy()
                settings_widgets.clear()
                self.what_page_am_i_on = "main_menu"
                self.__init__(self.master)  # Re-initialize to load the main menu

            back_btn = back_to_main_menu_button(self.master, settings_widgets, go_to_main_menu)
            back_btn.pack(pady=(10, 0))

        elif self.what_page_am_i_on == "about_me_and_help_menu":
            # all displays for about me and help menu here
            pass
            

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()