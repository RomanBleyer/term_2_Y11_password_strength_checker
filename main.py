import tkinter as tk
from tkinter import ttk

# File function imports
from password_enter_tab import create_password_entry
from copy_to_clipboard_button import copy_to_clipboard_button
from hide_unhide_password import hide_unhide_password_button
from frame_packing_organisation import main_menu_organisation
from password_generator_settings_button import password_generator_settings_button  # <-- Add this import

class PasswordStrengthChecker:
    def __init__(self, master):
        self.master = master

        self.master.resizable(False, False) # prevent resizing
        self.master.geometry(f"500x200+{self.master.winfo_screenwidth()-510}+{self.master.winfo_screenheight()-280}") # force window size and position when opened

        # Track which page we're on
        self.what_page_am_i_on = getattr(self, "what_page_am_i_on", "main_menu")

        if self.what_page_am_i_on == "main_menu":
            widgets = []
            title = ttk.Label(self.master, text="Password Strength Checker", font=("Segoe UI", 18, "bold"))
            title.pack(pady=(10, 5))
            widgets.append(title)
            entry_frame = main_menu_organisation(self.master)
            password_entry = create_password_entry(entry_frame, widgets)
            copy_btn = copy_to_clipboard_button(entry_frame, password_entry, widgets)
            password_entry.pack(side="left", padx=(5, 0))
            show_password_state = [True]
            eye_btn = hide_unhide_password_button(entry_frame, password_entry, widgets, show_password_state)
            eye_btn.pack(side="left", padx=(5, 0))

            def go_to_settings():
                for widget in widgets:
                    widget.destroy()
                widgets.clear()
                self.what_page_am_i_on = "password_generator_settings_menu"
                self.__init__(self.master)  # Re-initialize to load the settings menu

            settings_frame = tk.Frame(self.master)
            settings_frame.pack(pady=(10, 0), fill="x", expand=True)
            settings_btn = password_generator_settings_button(settings_frame, widgets, go_to_settings)
            settings_btn.pack(anchor="center")

        elif self.what_page_am_i_on == "password_generator_settings_menu":
            settings_widgets = []
            title = ttk.Label(self.master, text="Password Generator Settings", font=("Segoe UI", 18, "bold"))
            title.pack(pady=(10, 5))
            settings_widgets.append(title)
            # Add more settings widgets here, e.g.:
            # label = ttk.Label(self.master, text="Setting 1")
            # label.pack()
            # settings_widgets.append(label)
            # ... add more widgets as needed ...

        elif self.what_page_am_i_on == "about_me_and_help_menu":
            # all displays for about me and help menu here
            pass
            

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()