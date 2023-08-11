from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import cv2
import bcrypt
import time
import datetime
from PIL import Image, ImageTk

# Define the COLOUR scheme for the dark theme
BG_COLOUR = "#424242"
FG_COLOUR = "#F1F2F6"
TITLE_COLOUR = "#FB3640"
ENTRY_BG_COLOUR = "#424242"
ENTRY_FG_COLOUR = "#424242"
BUTTON_BG_COLOUR = "#424242"
BUTTON_FG_COLOUR = "#23967F"
MAIN_FONT = "Impact"
BUTTON_RADIUS = 20
ENTRY_RADIUS = 20

# ------------------- Security System -------------------

class SecuritySystem:
    def __init__(self, main_menu_window):
        self.main_menu_window = main_menu_window
        self.security_system_active = False
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")
        self.detection = False
        self.detection_stopped_time = None
        self.timer_started = False
        self.SECONDS_TO_RECORD_AFTER_DETECTION = 5
        self.frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.out = None

    def start_security_system(self):
        self.security_system_active = True
        print("Security System is ON")

    def stop_security_system(self):
        self.security_system_active = False
        print("Security System is OFF")

    def check_security(self):
        if self.security_system_active:
            _, frame = self.cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            bodies = self.body_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) + len(bodies) > 0:
                if not self.detection:
                    self.detection = True
                    current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                    self.out = cv2.VideoWriter(f"{current_time}.mp4", self.fourcc, 24, self.frame_size)
                    print("Started Recording!")
            elif self.detection:
                if self.timer_started:
                    if time.time() - self.detection_stopped_time >= self.SECONDS_TO_RECORD_AFTER_DETECTION:
                        self.detection = False
                        self.timer_started = False
                        self.out.release()
                        print('Stop Recording!')
                else:
                    self.timer_started = True
                    self.detection_stopped_time = time.time()

            if self.detection:
                self.out.write(frame)

            cv2.imshow("Camera", frame)

        self.main_menu_window.root.after(10, self.check_security)

    def release_camera(self):
        if self.cap is not None:
            self.cap.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()

# ------------------- Login Window -------------------

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")
        self.root.config(bg=BG_COLOUR)

        style = ttk.Style()
        style.configure("TButton", background=BUTTON_BG_COLOUR, foreground=BUTTON_FG_COLOUR, font=(MAIN_FONT, 10), relief="flat", borderwidth=0)
        style.map("TButton", background=[("active", "#555555")], foreground=[("active", BUTTON_BG_COLOUR)])

        self.login_label = Label(root, text="LOGIN", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.login_label.pack()

        self.username_label = Label(root, text="Username:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.username_label.pack()

        self.username_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.username_entry.pack(pady=5)

        self.password_label = Label(root, text="Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.password_label.pack()

        self.password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(root, text="Log In", command=self.login, style="TButton", width=15, cursor="hand2")
        self.login_button.pack(pady=10)

        self.register_button = ttk.Button(root, text="Register", command=self.open_registration, style="TButton", width=15, cursor="hand2")
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open("users.csv", "r") as file:
            for line in file:
                email, saved_username, saved_password_hash = line.strip().split(",")
                if username == saved_username and bcrypt.checkpw(password.encode(), saved_password_hash.encode()):
                    messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                    self.root.withdraw()
                    main_menu_window = Toplevel(self.root)
                    MainMenuWindow(main_menu_window, self)
                    return

        messagebox.showerror("Login Failed", "Invalid username or password")

    def open_registration(self):
        self.root.withdraw()
        registration_window = Toplevel(self.root)
        RegistrationWindow(registration_window, self.root)
        registration_window.protocol("WM_DELETE_WINDOW", lambda: self.back(registration_window))

    def back(self, window):
        window.destroy()
        self.root.deiconify()

# ------------------- Registration Window -------------------

class RegistrationWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.geometry("350x425")
        self.root.title("Registration")
        self.root.config(bg=BG_COLOUR)

        style = ttk.Style()
        style.configure("TEntry", fieldbackground=ENTRY_BG_COLOUR, foreground=ENTRY_FG_COLOUR, bordercolour=BUTTON_BG_COLOUR, borderwidth=0, focuscolour=BUTTON_BG_COLOUR)
        style.map("TEntry", background=[("active", ENTRY_BG_COLOUR)], relief=[("focus", "flat")])

        self.registration_label = Label(root, text="REGISTRATION", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.registration_label.pack()

        self.email_label = Label(root, text="Email:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.email_label.pack()

        self.email_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.email_entry.pack(pady=5)

        self.username_label = Label(root, text="Username:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.username_label.pack()

        self.username_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.username_entry.pack(pady=5)

        self.password_label = Label(root, text="Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.password_label.pack()

        self.password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.password_entry.pack(pady=5)

        self.confirm_password_label = Label(root, text="Confirm Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.confirm_password_entry.pack(pady=5)

        self.blank_line = Label(root, text="", bg=BG_COLOUR, fg=FG_COLOUR)
        self.blank_line.pack()

        self.register_button = ttk.Button(root, text="Register", command=self.register, style="TButton", width=15, cursor="hand2")
        self.register_button.pack(pady=5)

        self.delete_button = ttk.Button(root, text="Delete User", command=self.delete_user_confirm, style="TButton", width=15, cursor="hand2")
        self.delete_button.pack(pady=5)

        self.back_button = ttk.Button(root, text="Back", command=self.back, style="TButton", width=15, cursor="hand2")
        self.back_button.pack(pady=5)

    def register(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not (email and username and password and confirm_password):
            messagebox.showerror("Error", "Please fill in all fields")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        elif not self.is_valid_email(email):
            messagebox.showerror("Error", "Invalid email address")
        elif not self.is_strong_password(password):
            messagebox.showerror("Error", "Password must be at least 8 characters long and contain uppercase, lowercase, digit, and special character.")
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            with open("users.csv", "a") as file:
                file.write(f"{email},{username},{hashed_password}\n")

            messagebox.showinfo("Registration Successful", "You have been registered successfully")
            self.clear_fields()

    def delete_user_confirm(self):
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if response:
            self.delete_user()

    def delete_user(self):
        username = self.username_entry.get()
        lines = []

        with open("users.csv", "r") as file:
            for line in file:
                email, saved_username, _ = line.strip().split(",")
                if username != saved_username:
                    lines.append(line)

        with open("users.csv", "w") as file:
            file.writelines(lines)

        messagebox.showinfo("User Deleted", f"The user '{username}' has been deleted")
        self.clear_fields()

    def back(self):
        self.root.withdraw()
        self.login_window.deiconify()

    def clear_fields(self):
        self.email_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)

    def is_valid_email(self, email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def is_strong_password(self, password):
        return any(char.isupper() for char in password) and \
               any(char.islower() for char in password) and \
               any(char.isdigit() for char in password) and \
               any(not char.isalnum() for char in password)

# ------------------- Main Menu Window -------------------

class MainMenuWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.geometry("400x250")  # Set window size
        self.root.title("Main Menu")
        self.root.config(bg=BG_COLOUR)  # Set background colour

        self.title_label = Label(root, text="Main Menu", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.title_label.pack(pady=10)

        self.live_view_button = ttk.Button(root, text="Live View", command=self.open_live_view, style="TButton", width=15, cursor="hand2")
        self.live_view_button.pack(pady=5)

        self.activity_log_button = ttk.Button(root, text="View Activity Log", command=self.open_activity_log, style="TButton", width=20, cursor="hand2")
        self.activity_log_button.pack(pady=5)

        self.print_report_button = ttk.Button(root, text="Print Report", command=self.open_print_report, style="TButton", width=15, cursor="hand2")
        self.print_report_button.pack(pady=5)

        self.exit_button = ttk.Button(root, text="Exit", command=self.exit_program, style="TButton", width=15, cursor="hand2")
        self.exit_button.pack(pady=5)

        self.security_button_text = StringVar()
        self.security_button_text.set("Turn On Security System")
        self.security_button = ttk.Button(root, textvariable=self.security_button_text, command=self.toggle_security_system, style="TButton", width=20, cursor="hand2")
        self.security_button.pack(pady=5)

        self.video_feed_label = Label(root, bg=BG_COLOUR)
        self.video_feed_label.pack()

        self.security_system = SecuritySystem(self)
        self.security_system.check_security()

    def update_video_feed(self, label):
        _, frame = self.security_system.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        label.imgtk = photo
        label.configure(image=photo)
        label.after(10, lambda: self.update_video_feed(label))

    def open_live_view(self):
        live_view_window = Toplevel(self.root)
        live_view_window.title("Live View")
        live_view_window.geometry("400x300")
        live_view_window.config(bg=BG_COLOUR)

        video_feed_label = Label(live_view_window, bg=BG_COLOUR)
        video_feed_label.pack()
        self.update_video_feed(video_feed_label)

    def open_activity_log(self):
        activity_log_window = Toplevel(self.root)
        activity_log_window.title("Activity Log")
        activity_log_window.geometry("400x200")
        activity_log_window.config(bg=BG_COLOUR)
        Label(activity_log_window, text="This is the Activity Log window", font=(MAIN_FONT, 14), bg=BG_COLOUR,
              fg=FG_COLOUR).pack(pady=30)

    def open_print_report(self):
        print_report_window = Toplevel(self.root)
        print_report_window.title("Print Report")
        print_report_window.geometry("400x200")
        print_report_window.config(bg=BG_COLOUR)
        Label(print_report_window, text="This is the Print Report window", font=(MAIN_FONT, 14), bg=BG_COLOUR,
              fg=FG_COLOUR).pack(pady=30)

    def toggle_security_system(self):
        if self.security_system.security_system_active:
            self.security_system.stop_security_system()
            self.security_button_text.set("Turn On Security System")
        else:
            self.security_system.start_security_system()
            self.security_button_text.set("Turn Off Security System")

    def exit_program(self):
        self.security_system.release_camera()  # Release camera resources
        self.root.withdraw()  # Hide the current window
        self.login_window.root.deiconify()  # Show the login window

if __name__ == "__main__":
    root = Tk()
    root.config(bg=BG_COLOUR)
    login_window = LoginWindow(root)

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if hasattr(login_window, 'main_menu_window'):
                main_menu_window = login_window.main_menu_window
                if main_menu_window.security_system.security_system_active:
                    main_menu_window.security_system.release_camera()
                main_menu_window.exit_program()  # Call the exit_program method

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()