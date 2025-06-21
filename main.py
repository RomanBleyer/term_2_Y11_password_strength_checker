import tkinter as tk
from tkinter import ttk

# File function imports
from password_enter_tab import create_password_entry
from copy_to_clipboard_button import copy_to_clipboard_button
from hide_unhide_password import hide_unhide_password_button
from password_generator_settings_button import password_generator_settings_button
from back_to_main_menu_button import back_to_main_menu_button
from password_generation_settings import create_password_generation_settings
from about_us_tab import about_us_button
from about_us_window import show_about_us_window
class PasswordStrengthChecker:
    def __init__(self, master):
        self.master = master

        self.master.resizable(False, False)
        self.master.geometry(f"500x200+{self.master.winfo_screenwidth()-510}+{self.master.winfo_screenheight()-280}")

        # Track which page we're on
        self.what_page_am_i_on = getattr(self, "what_page_am_i_on", "main_menu")

        # Only initialize settings_state if it doesn't exist yet
        if not hasattr(self, "settings_state"):
            self.settings_state = {
                "use_capital_letters": True,
                "use_special_characters": True,
                "use_numbers": True,
                "copy_after_generation": True,
                "check_strength_after_generation": True
            }

        if self.what_page_am_i_on == "main_menu":
            # Destroy all widgets from previous menu
            if hasattr(self, 'widgets'):
                for widget in self.widgets:
                    widget.destroy()
            self.widgets = []

            # Unbind any previous <Return> events
            self.master.unbind('<Return>')

            widgets = []
            # Title
            title = ttk.Label(self.master, text="Password Strength Checker", font=("Segoe UI", 18, "bold"))
            title.place(relx=0.5, y=10, anchor="n")  # Centered horizontally at the top
            widgets.append(title)

            # Entry row frame
            entry_frame = tk.Frame(self.master)
            entry_frame.place(x=40, y=60, width=420, height=40)
            widgets.append(entry_frame)

            # Entry row widgets
            copy_btn = copy_to_clipboard_button(entry_frame, None, widgets)
            # Persistent StringVar for password entry
            self.password_var = getattr(self, 'password_var', tk.StringVar())
            password_entry = create_password_entry(entry_frame, widgets, textvariable=self.password_var)
            show_password_state = [True]
            eye_btn = hide_unhide_password_button(entry_frame, password_entry, widgets, show_password_state)

            # Center the password bar (entry) in the entry_frame
            copy_btn.place(x=25, y=0, width=40, height=40)  # 25px from the left, aligned with password bar
            password_entry.place(x=70, y=0, width=280, height=40)  # Centered in 420px frame: (420-280)/2 = 70
            eye_btn.place(x=355, y=0, width=40, height=40)  # 420-40-25 = 355

            # --- Controls row under the password bar ---
            controls_y = 110  # y position under the password bar

            # Define go_to_settings BEFORE using it
            def go_to_settings():
                for widget in widgets:
                    widget.destroy()
                widgets.clear()
                self.what_page_am_i_on = "password_generator_settings_menu"
                self.__init__(self.master)

            # Settings button (leftmost)
            settings_btn2 = password_generator_settings_button(self.master, widgets, go_to_settings)
            settings_btn2.place(x=40, y=controls_y, width=40, height=40)

            # Generate Password button (big)
            def on_generate():
                # You can implement password generation logic here
                pass  # Replace with your logic

            generate_btn = tk.Button(self.master, text="Generate Password", font=("Segoe UI", 12, "bold"), command=on_generate)
            generate_btn.place(x=90, y=controls_y, width=160, height=40)
            widgets.append(generate_btn)

            # Entry for password length (default 12)
            self.length_var = getattr(self, 'length_var', tk.StringVar(value="12"))
            length_entry = tk.Entry(self.master, textvariable=self.length_var, width=4, font=("Segoe UI", 12), justify="center")
            length_entry.place(x=260, y=controls_y+7, width=40, height=26)
            widgets.append(length_entry)

            # Label for "maximum 16 characters"
            max_label = ttk.Label(self.master, text="maximum 16 characters", font=("Segoe UI", 10))
            max_label.place(x=310, y=controls_y+10)
            widgets.append(max_label)

            # --- Check Password button centered under controls row ---
            check_btn = tk.Button(
                self.master,
                text="Check Password",
                font=("Segoe UI", 12, "bold"),
                command=lambda: print("Check password logic here")  # Replace with your logic
            )
            # Centered horizontally: window width is 500, button width is 160
            check_btn.place(x=170, y=controls_y+45, width=160, height=40)  # moved up by 10px
            widgets.append(check_btn)

            # About button (rightmost)
            def go_to_about():
                for widget in widgets:
                    widget.destroy()
                widgets.clear()
                self.what_page_am_i_on = "about_me_and_help_menu"
                self.__init__(self.master)

            about_btn = about_us_button(self.master, widgets, go_to_about)
            widgets.append(about_btn)

        elif self.what_page_am_i_on == "password_generator_settings_menu":
            # Destroy all widgets from previous menu
            if hasattr(self, 'settings_widgets'):
                for widget in self.settings_widgets:
                    widget.destroy()
            self.settings_widgets = []

            self.master.unbind('<Return>')

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
            def return_to_main_menu():
                self.what_page_am_i_on = "main_menu"
                self.__init__(self.master)
            show_about_us_window(self.master, return_to_main_menu)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordStrengthChecker(root)
    root.mainloop()