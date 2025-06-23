# --- Imports ---
import tkinter as tk
from PIL import Image, ImageTk
import os
import string
import random
import math
import nltk
from pwnedpasswords import check

nltk.download('words', quiet=True)
from nltk.corpus import words

DARK_BLUE = "#102040"
WHITE = "#ffffff"

# --- Helper: Loads and converts any image to white ---

def load_white_icon(path, size=(32, 32)):
    """
    Loads an image, resizes it, and converts all non-transparent pixels to white.
    Returns a Tkinter PhotoImage.
    """
    img = Image.open(path).convert("RGBA").resize(size)
    datas = img.getdata()
    newData = []
    for item in datas:
        # If pixel is not transparent, make it white (keep alpha)
        if item[3] > 0:
            newData.append((255, 255, 255, item[3]))
        else:
            newData.append(item)
    img.putdata(newData)
    return ImageTk.PhotoImage(img)

# --- Password Entry Field ---

def create_password_entry(parent, widgets, textvariable=None):
    if textvariable is None:
        textvariable = tk.StringVar()
    password_entry = tk.Entry(
        parent, width=30, font=("Segoe UI", 16, "bold"),
        foreground=WHITE, background=DARK_BLUE, insertbackground=WHITE,
        justify="center", textvariable=textvariable
    )
    widgets.append(password_entry)

    # No spaces allowed and max 16 characters
    def validate_entry(new_value):
        return (' ' not in new_value) and (len(new_value) <= 16)

    vcmd = (parent.register(validate_entry), '%P')
    password_entry.config(validate="key", validatecommand=vcmd)

    return password_entry

# --- Copy to Clipboard Button ---

def copy_to_clipboard_button(parent, password_entry, widgets):
    icon_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "copy_to_clipboard.png")
    copy_to_clipboard_image = load_white_icon(icon_path, size=(32, 32))

    def copy_to_clipboard():
        password = password_entry.get()
        parent.clipboard_clear()
        parent.clipboard_append(password)

    copy_btn = tk.Button(parent, image=copy_to_clipboard_image, command=copy_to_clipboard,
    bg=DARK_BLUE, activebackground=DARK_BLUE, borderwidth=0)
    copy_btn.image = copy_to_clipboard_image
    widgets.append(copy_btn)
    return copy_btn

# --- Hide/Unhide Password Button ---

def hide_unhide_password_button(parent, password_entry, widgets, show_password_state):
    base_path = os.path.join(os.path.dirname(__file__), "password_checker_images")
    eye_open_image = load_white_icon(os.path.join(base_path, "eye_open.png"), size=(32, 32))
    eye_closed_image = load_white_icon(os.path.join(base_path, "eye_closed.png"), size=(32, 32))

    def toggle_password_visibillity():
        if show_password_state[0] is True:
            show_password_state[0] = False
            password_entry.config(show="•")
            toggle_btn.config(image=eye_closed_image)
        else:
            show_password_state[0] = True
            password_entry.config(show="")
            toggle_btn.config(image=eye_open_image)

    if show_password_state[0] is True:
        password_entry.config(show="")
        initial_image = eye_open_image
    else:
        password_entry.config(show="•")
        initial_image = eye_closed_image

    toggle_btn = tk.Button(parent, image=initial_image, command=toggle_password_visibillity,
                          bg=DARK_BLUE, activebackground=DARK_BLUE, borderwidth=0)
    toggle_btn.image_open = eye_open_image
    toggle_btn.image_closed = eye_closed_image
    widgets.append(toggle_btn)
    return toggle_btn

# --- Settings (Gear) Button ---

def password_generator_settings_button(master, widgets, go_to_settings_callback):
    icon_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "settings_gear.png")
    settings_image = load_white_icon(icon_path, size=(30, 30))

    settings_button = tk.Button(
        master,
        image=settings_image,
        command=go_to_settings_callback,
        borderwidth=0,
        bg=DARK_BLUE,
        activebackground=DARK_BLUE
    )
    settings_button.image = settings_image
    widgets.append(settings_button)
    return settings_button

# --- Settings Menu Toggle Buttons ---

def create_password_generation_settings(master, widgets, state):
    labels = {
        "use_capital_letters": "Use Capital Letters",
        "use_special_characters": "Use Special Characters",
        "use_numbers": "Use Numbers",
        "copy_after_generation": "Copy After Generation",
        "check_strength_after_generation": "Check Strength After Generation"
    }
    buttons = {}

    for key, label in labels.items():
        def toggle(k=key):
            state[k] = not state[k]
            buttons[k].config(text=f"{labels[k]}: {state[k]}")
        btn = tk.Button(
            master,
            text=f"{label}: {state[key]}",
            command=toggle,
            font=("Segoe UI", 10, "bold"),
            width=30,
            bg=DARK_BLUE,
            fg=WHITE,
            activebackground=DARK_BLUE,
            activeforeground=WHITE
        )
        widgets.append(btn)
        buttons[key] = btn

    return buttons

# --- Password Length Entry ---

def create_length_entry(parent, widgets, textvariable=None): # makes the password length entry which only accepts numbers from 1 to 16
    def validate_number(P):
        if P == "":
            return True
        if P.isdigit():
            value = int(P)
            return 1 <= value <= 16
        return False
    if textvariable is None:
        textvariable = tk.StringVar(value="12")
    vcmd = (parent.register(validate_number), "%P")
    length_entry = tk.Entry(
        parent,
        textvariable=textvariable,
        width=4,
        font=("Segoe UI", 12, "bold"),
        justify="center",
        validate="key",
        validatecommand=vcmd,
        background=DARK_BLUE,
        foreground=WHITE,
        insertbackground=WHITE
    )
    widgets.append(length_entry)
    return length_entry, textvariable

# --- About Us Button ---

def about_us_button(master, widgets, go_to_about_callback):
    image_path = os.path.join(os.path.dirname(__file__), "password_checker_images", "about_us.png")
    photo = load_white_icon(image_path, size=(30, 30))
    button = tk.Button(master, image=photo, command=go_to_about_callback, borderwidth=0,
    bg=DARK_BLUE, activebackground=DARK_BLUE)
    button.image = photo
    widgets.append(button)
    return button

# --- END BUTTON CREATION FUNCTIONS ---

# --- About Us Window code generation ---

def show_about_us_window(master, widgets, return_to_main_menu_callback): # creates the about us window widgets, the title, description and the fine print for how to exit
    title = tk.Label(master, text="About this Program", font=("Segoe UI", 16, "bold"),
    bg=DARK_BLUE, fg=WHITE)
    title.place(relx=0.5, y=20, anchor="center")
    widgets.append(title)

    desc = tk.Label(
        master,
        text="This program was created by Roman Bleyer,\nit allows you to check the strength of your password using various\ndatabases or generate a password based on a bunch of settings. Enjoy!",
        font=("Segoe UI", 12),
        justify="center",
        anchor="center",
        bg=DARK_BLUE,
        fg=WHITE
    )
    desc.place(relx=0.5, y=70, anchor="center")
    widgets.append(desc)

    fine_print = tk.Label(master, text="press enter to return to the main menu",
    font=("Segoe UI", 8, "bold", "italic"),
    bg=DARK_BLUE, fg=WHITE)
    fine_print.place(relx=0.5, rely=1.0, y=-20, anchor="s")
    widgets.append(fine_print)

    def on_enter(event):
        for widget in widgets:
            widget.destroy()
        widgets.clear()
        master.unbind('<Return>')
        return_to_main_menu_callback()

    master.bind('<Return>', on_enter)

# --- PASSWORD GENERATION LOGIC ---

def generate_password(settings, length): # logic to generate a password based on the settings and length
    chars = string.ascii_lowercase
    if settings.get("use_capital_letters", True):
        chars += string.ascii_uppercase
    if settings.get("use_numbers", True):
        chars += string.digits
    if settings.get("use_special_characters", True):
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>/?"
    if not chars:
        chars = string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))

# --- PASSWORD STRENGTH CHECKING LOGIC ---
# contains a large amount of frankly confusing math, but seems to be working so I will not poke the beast
COMMON_PATH = os.path.join(os.path.dirname(__file__), "commonly_used_passwords.txt")
with open(COMMON_PATH, encoding="utf-8") as file:
    COMMON_PASSWORDS = {line.strip().lower() for line in file if line.strip()}

DICTIONARY = {w.lower() for w in words.words() if len(w) >= 4}

def estimate_crack_time_years(pwd):
    charset = (
        (26 if any(c.islower() for c in pwd) else 0) +
        (26 if any(c.isupper() for c in pwd) else 0) +
        (10 if any(c.isdigit() for c in pwd) else 0) +
        (len(string.punctuation) if any(c in string.punctuation for c in pwd) else 0)
    ) or 1

    entropy = len(pwd) * math.log2(charset)
    years = (2 ** entropy) / (1e10 * 60 * 60 * 24 * 365)
    return years

def check_password(password):
    pwd = password.strip()
    results = []

    # Length checks
    if len(pwd) < 8:
        results.append("❌ Too short (min 8).")
    else:
        results.append("✔️ Length OK.")

    # check if it is a common password
    results.append("❌ Common password!" if pwd.lower() in COMMON_PASSWORDS else "✔️ Not common.")

    # check if it contains a dictionary word (4+ letters)
    found = next((w for w in DICTIONARY if w in pwd.lower()), None)
    results.append(f"❌ Contains word: '{found}'" if found else "✔️ No dictionary words.")

    # check if password is breached
    try:
        count = check(pwd)
        results.append(f"❌ Found in breaches: {count}" if count else "✔️ Not breached.")
    except Exception as e:  # if it somehow fails
        results.append(f"⚠️ Breach check failed: {e}")

    # Crack strength
    years = estimate_crack_time_years(pwd)
    if years > 1e6:
        tag = "✔️ Very strong"
    elif years > 100:
        tag = "⚠️ Strong"
    elif years > 1:
        tag = "⚠️ Moderate"
    else:
        tag = "❌ Weak"
    results.append(f"{tag} — {years:.2f} years to crack.")

    return "\n".join(results)

def show_password_check_window(master, result_text):  # creates a new window to show the password check results
    win = tk.Toplevel(master)
    win.title("Password Check Result")
    win.resizable(False, False)
    win.configure(bg=DARK_BLUE)
    master.update_idletasks()

    # Set window size
    win_w, win_h = 300, 180

    # Center the window over the main window
    main_x = master.winfo_x()
    main_y = master.winfo_y()
    main_w = master.winfo_width()
    main_h = master.winfo_height()
    x = main_x + (main_w // 2) - (win_w // 2)
    y = main_y + (main_h // 2) - (win_h // 2)
    win.geometry(f"{win_w}x{win_h}+{x}+{y}")

    # Use a Text widget for colored output
    text = tk.Text(win, font=("Segoe UI", 10, "bold"), wrap="word", height=6, width=36, state="normal",
    bg=DARK_BLUE, fg=WHITE, insertbackground=WHITE)
    text.pack(padx=10, pady=10, fill="both", expand=True)

    # Define tags for coloring
    text.tag_configure("good", foreground="green", font=("Segoe UI", 10, "bold"))
    text.tag_configure("bad", foreground="red", font=("Segoe UI", 10, "bold"))
    text.tag_configure("warn", foreground="orange", font=("Segoe UI", 10, "bold"))
    text.tag_configure("default", foreground=WHITE, font=("Segoe UI", 10, "bold"))

    # Insert each line with the appropriate color
    for line in result_text.splitlines():
        if "✔️" in line:
            tag = "good"
        elif "❌" in line:
            tag = "bad"
        elif "⚠️" in line:
            tag = "warn"
        else:
            tag = "default"
        text.insert("end", line + "\n", tag)

    text.config(state="disabled")  # Make the text box read-only

    close_btn = tk.Button(win, text="Close", command=win.destroy,
    font=("Segoe UI", 10, "bold"),
    bg=DARK_BLUE, fg=WHITE, activebackground=DARK_BLUE, activeforeground=WHITE)
    close_btn.pack(pady=(0, 10))

# --- MAIN APPLICATION CLASS ---

class PasswordStrengthChecker:
    def __init__(self, master):
        self.master = master
        self.master.resizable(False, False)
        self.master.geometry(f"500x200+{self.master.winfo_screenwidth()-510}+{self.master.winfo_screenheight()-280}")
        self.master.configure(bg=DARK_BLUE)

        self.what_page_am_i_on = "main_menu"
        self.settings_state = {
            "use_capital_letters": True,
            "use_special_characters": True,
            "use_numbers": True,
            "copy_after_generation": False,
            "check_strength_after_generation": False
        }
        self.widgets = []
        self.settings_widgets = []
        self.password_var = tk.StringVar()
        self.length_var = tk.StringVar(value="12")

        self.route_page()

    def route_page(self):
        if self.what_page_am_i_on == "main_menu":
            self.show_main_menu()
        elif self.what_page_am_i_on == "password_generator_settings_menu":
            self.show_settings_menu()
        elif self.what_page_am_i_on == "about_me_and_help_menu":
            self.show_about_menu()

    def clear_widgets(self, widget_list):
        for widget in widget_list:
            try:
                widget.destroy()
            except Exception:
                pass
        widget_list.clear()

    def show_main_menu(self):
        self.clear_widgets(self.widgets)
        self.master.unbind('<Return>')
        widgets = self.widgets

        # Main title
        title = tk.Label(self.master, text="Password Strength Checker", font=("Segoe UI", 18, "bold"),
        bg=DARK_BLUE, fg=WHITE)
        title.place(relx=0.5, y=10, anchor="n")
        widgets.append(title)

        # Entry frame
        entry_frame = tk.Frame(self.master, bg=DARK_BLUE)
        entry_frame.place(x=40, y=60, width=420, height=40)
        widgets.append(entry_frame)

        password_entry = create_password_entry(entry_frame, widgets, textvariable=self.password_var)
        copy_btn = copy_to_clipboard_button(entry_frame, password_entry, widgets)
        show_password_state = [True]
        eye_btn = hide_unhide_password_button(entry_frame, password_entry, widgets, show_password_state)

        copy_btn.place(x=25, y=0, width=40, height=40)
        password_entry.place(x=70, y=0, width=280, height=40)
        eye_btn.place(x=355, y=0, width=40, height=40)

        # --- Controls row under the password bar ---
        

        def go_to_settings():
            self.what_page_am_i_on = "password_generator_settings_menu"
            self.route_page()

        settings_btn2 = password_generator_settings_button(self.master, widgets, go_to_settings)
        settings_btn2.place(x=40, y=110, width=40, height=40)

        length_entry, _ = create_length_entry(self.master, widgets, textvariable=self.length_var)
        length_entry.place(x=260, y=110+7, width=40, height=26)

        # Generate Password button
        def on_generate():
            try:
                length = int(self.length_var.get())
            except ValueError:
                length = 12
            pwd = generate_password(self.settings_state, length)
            self.password_var.set(pwd)
            # Copy after generation
            if self.settings_state.get("copy_after_generation"):
                self.master.clipboard_clear()
                self.master.clipboard_append(pwd)
            # Check strength after generation
            if self.settings_state.get("check_strength_after_generation"):
                show_password_check_window(self.master, check_password(pwd))

        generate_btn = tk.Button(self.master, text="Generate Password", font=("Segoe UI", 12, "bold"),
        command=on_generate, bg=DARK_BLUE, fg=WHITE,
        activebackground=DARK_BLUE, activeforeground=WHITE)
        generate_btn.place(x=90, y=110, width=160, height=40)
        widgets.append(generate_btn)

        # Label for "maximum 16 characters"
        max_label = tk.Label(self.master, text="maximum 16 characters", font=("Segoe UI", 10, "bold"),
        bg=DARK_BLUE, fg=WHITE)
        max_label.place(x=310, y=110+10)
        widgets.append(max_label)

        # Check Password button
        check_btn = tk.Button(
            self.master,
            text="Check Password",
            font=("Segoe UI", 12, "bold"),
            command=lambda: show_password_check_window(self.master, check_password(self.password_var.get())),
            bg=DARK_BLUE, fg=WHITE, activebackground=DARK_BLUE, activeforeground=WHITE
        )
        check_btn.place(x=170, y=110+45, width=160, height=40)
        widgets.append(check_btn)

        def go_to_about():
            self.what_page_am_i_on = "about_me_and_help_menu"
            self.route_page()

        about_btn = about_us_button(self.master, widgets, go_to_about)
        about_btn.place(x=10, y=10, width=40, height=40)
        widgets.append(about_btn)

    def show_settings_menu(self):
        self.clear_widgets(self.widgets)
        self.clear_widgets(self.settings_widgets)
        self.master.unbind('<Return>')
        settings_widgets = self.settings_widgets

        buttons = create_password_generation_settings(self.master, settings_widgets, self.settings_state)
        y_offset = 5
        for idx, btn in enumerate(buttons.values()):
            btn.place(x=100, y=y_offset + idx * 28, width=300, height=25)

        small_print = tk.Label(self.master, text="press enter to return to the main menu",
        font=("Segoe UI", 8, "bold", "italic"),
        bg=DARK_BLUE, fg=WHITE)
        small_print.place(x=140, y=y_offset + 5 * 28 + 10)
        settings_widgets.append(small_print)

        def on_enter(event):
            self.clear_widgets(settings_widgets)
            self.what_page_am_i_on = "main_menu"
            self.route_page()
        self.master.bind('<Return>', on_enter)

    def show_about_menu(self):
        def return_to_main_menu():
            self.what_page_am_i_on = "main_menu"
            self.route_page()
        self.clear_widgets(self.widgets)
        show_about_us_window(self.master, self.widgets, return_to_main_menu)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Password Strength Checker") 
    app = PasswordStrengthChecker(root)
    root.mainloop()