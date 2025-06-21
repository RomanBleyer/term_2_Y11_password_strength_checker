import tkinter as tk
from tkinter import ttk

# File function imports
from password_enter_tab import create_password_entry

class PasswordStrengthChecker:
    def __init__(self, master):
        self.master = master

        self.master.resizable(False, False) # prevent resizing
        self.master.geometry(f"500x200+{self.master.winfo_screenwidth()-510}+{self.master.winfo_screenheight()-280}") # force window size and position when opened

        # ------------------------------------------------------------------ #

        self.what_page_am_i_on = "main_menu"

        if self.what_page_am_i_on == "main_menu":
            title = ttk.Label(self.master, text="Password Strength Checker", font=("Segoe UI", 18, "bold"))
            title.pack(pady=(10, 5)) # use pack to force centering
            create_password_entry(self.master, [])
            
        elif self.what_page_am_i_on == "password_generator_settings_menu":
            # all displays for password generator settings menu here
            pass
        elif self.what_page_am_i_on == "about_me_and_help_menu":
            # all displays for about me and help menu here
            pass
            

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()