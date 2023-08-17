from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox
import cv2
import bcrypt
import time
import datetime
from PIL import Image, ImageTk
import re
import os
from tkinter import scrolledtext
import win32print
import win32con
import pywintypes

# Define the colour scheme for the dark theme
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

# -------- Security System ---------
class SecuritySystem:
    # Defining all preliminary variables
    def __init__(self, root):
        self.root = root
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

        self.activity_folder = "Activity"
        if not os.path.exists(self.activity_folder):
            os.mkdir(self.activity_folder)
        
        self.cleanup_activity_folder()

    # Starting Security System
    def start_security_system(self):
        self.security_system_active = True
        print("Security System is ON")

    # Stopping Security System
    def stop_security_system(self):
        self.security_system_active = False
        print("Security System is OFF")

    # Security System Logic
    def check_security(self):
        if self.security_system_active:
            _, frame = self.cap.read()
            grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Converts frame to greyscale to use haarcascades
            faces = self.face_cascade.detectMultiScale(grey, 1.3, 5) # Face haarcascade
            bodies = self.body_cascade.detectMultiScale(grey, 1.3, 5) # Body haarcascade

            if len(faces) + len(bodies) > 0: # If faces or bodies are in the frame
                if not self.detection: # If not already recording
                    self.detection = True # Start recording
                    current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                    video_filename = os.path.join(self.activity_folder, f"{current_time}.mp4")
                    self.out = cv2.VideoWriter(video_filename, self.fourcc, 24, self.frame_size) # Specs for exported videos
                    self.write_activity_text_file(current_time) # Save timestamp to text file
                    print("Started Recording!")
            elif self.detection: # If already recording
                if self.timer_started: # If timer has started
                    if time.time() - self.detection_stopped_time >= self.SECONDS_TO_RECORD_AFTER_DETECTION: # If time since last body or face in frame has been more than or equal to recording threshold
                        self.detection = False # Stop recording
                        self.timer_started = False # Reset variable
                        self.out.release() # Release resource
                        print('Stop Recording!')
                else: # If timer has not started
                    self.timer_started = True # Start timer
                    self.detection_stopped_time = time.time()

            if self.detection:
                self.out.write(frame) # Write to file

            cv2.imshow("Camera", frame) # Show original frame view

        self.root.after(10, self.check_security)

    # Function to release resources
    def release_camera(self):
        if self.cap is not None:
            self.cap.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()
    
    # Writing to text files
    def write_activity_text_file(self, current_time):
        text_filename = os.path.join(self.activity_folder, f"{current_time}.txt") # Find file
        with open(text_filename, "w") as file:
            file.write("Activity Details:\n") # Populate file
            file.write(f"Start Time: {current_time}\n") # Populate file
    
    # Deleting old files
    def cleanup_activity_folder(self):
        max_activity_age_days = 60  # Age threshold of recordings
        now = time.time()
        for filename in os.listdir(self.activity_folder):
            file_path = os.path.join(self.activity_folder, filename)
            if os.path.isfile(file_path):
                file_age_days = (now - os.path.getctime(file_path)) / (60 * 60 * 24)
                if file_age_days > max_activity_age_days: # If file age is past threshold
                    os.remove(file_path) # Delete file
                    print(f"Removed old file: {filename}") # Notify that file has been deleted

# -------- App --------
class App:
    # Defining preliminary variables
    def __init__(self, root):
        self.root = root
        self.root.title("Security App")
        self.root.geometry("800x600")
        self.root.config(bg=BG_COLOUR)

        # Set style
        style = ttk.Style()
        style.configure("TButton", background=BUTTON_BG_COLOUR, foreground=BUTTON_FG_COLOUR, font=(MAIN_FONT, 10), relief="flat", borderwidth=0)
        style.map("TButton", background=[("active", "#555555")], foreground=[("active", BUTTON_BG_COLOUR)])

        self.security_system = SecuritySystem(self.root)
        self.security_system.check_security()

        self.current_screen = None
        self.create_login_screen()

    # Creating Login Screen
    def create_login_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = Frame(self.root, bg=BG_COLOUR)
        self.current_screen.pack(fill=BOTH, expand=True)

        self.login_label = Label(self.current_screen, text="LOGIN", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.login_label.pack()

        self.username_label = Label(self.current_screen, text="Username:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.username_label.pack()

        self.username_entry = ttk.Entry(self.current_screen, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.username_entry.pack(pady=5)

        self.password_label = Label(self.current_screen, text="Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.password_label.pack()

        self.password_entry = ttk.Entry(self.current_screen, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.password_entry.pack(pady=5)

        self.login_button = ttk.Button(self.current_screen, text="Log In", command=self.login, style="TButton", width=15, cursor="hand2")
        self.login_button.pack(pady=10)

        self.register_button = ttk.Button(self.current_screen, text="Register", command=self.create_registration_screen, style="TButton", width=15, cursor="hand2")
        self.register_button.pack()

    # Creating Registration Screen
    def create_registration_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = Frame(self.root, bg=BG_COLOUR)
        self.current_screen.pack(fill=BOTH, expand=True)

        self.registration_label = Label(self.current_screen, text="REGISTRATION", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.registration_label.pack()

        self.email_label = Label(self.current_screen, text="Email:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.email_label.pack()

        self.email_entry = ttk.Entry(self.current_screen, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.email_entry.pack(pady=5)

        self.username_label = Label(self.current_screen, text="Username:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.username_label.pack()

        self.username_entry = ttk.Entry(self.current_screen, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.username_entry.pack(pady=5)

        self.password_label = Label(self.current_screen, text="Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.password_label.pack()

        self.password_entry = ttk.Entry(self.current_screen, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.password_entry.pack(pady=5)

        self.confirm_password_label = Label(self.current_screen, text="Confirm Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(self.current_screen, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.confirm_password_entry.pack(pady=5)

        self.blank_line = Label(self.current_screen, text="", bg=BG_COLOUR, fg=FG_COLOUR)
        self.blank_line.pack()

        self.register_button = ttk.Button(self.current_screen, text="Register", command=self.register, style="TButton", width=15, cursor="hand2")
        self.register_button.pack(pady=5)

        self.delete_button = ttk.Button(self.current_screen, text="Delete User", command=self.delete_user_confirm, style="TButton", width=15, cursor="hand2")
        self.delete_button.pack(pady=5)

        self.back_button = ttk.Button(self.current_screen, text="Back", command=self.create_login_screen, style="TButton", width=15, cursor="hand2")
        self.back_button.pack(pady=5)

    # Login Logic
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        with open("users.csv", "r") as file:
            for line in file:
                email, saved_username, saved_password_hash = line.strip().split(",")
                if username == saved_username and bcrypt.checkpw(password.encode(), saved_password_hash.encode()):
                    messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                    self.create_main_menu_screen()
                    return

        messagebox.showerror("Login Failed", "Invalid username or password")

    # Creating Main Menu Screen
    def create_main_menu_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = Frame(self.root, bg=BG_COLOUR)
        self.current_screen.pack(fill=BOTH, expand=True)

        self.title_label = Label(self.current_screen, text="Main Menu", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.title_label.pack(pady=10)

        self.live_view_button = ttk.Button(self.current_screen, text="Live View", command=self.open_live_view, style="TButton", width=15, cursor="hand2")
        self.live_view_button.pack(pady=5)

        self.activity_log_button = ttk.Button(self.current_screen, text="View Activity Log", command=self.open_activity_log, style="TButton", width=20, cursor="hand2")
        self.activity_log_button.pack(pady=5)

        self.print_report_button = ttk.Button(self.current_screen, text="Print Report", command=self.open_print_report, style="TButton", width=15, cursor="hand2")
        self.print_report_button.pack(pady=5)

        self.exit_button = ttk.Button(self.current_screen, text="Exit", command=self.exit_program, style="TButton", width=15, cursor="hand2")
        self.exit_button.pack(pady=5)

        self.security_button_text = StringVar()
        self.security_button_text.set("Turn On Security System")
        self.security_button = ttk.Button(self.current_screen, textvariable=self.security_button_text, command=self.toggle_security_system, style="TButton", width=25, cursor="hand2")
        self.security_button.pack(pady=5)

        self.video_feed_label = Label(self.current_screen, bg=BG_COLOUR)
        self.video_feed_label.pack()

        self.update_video_feed(self.video_feed_label)

    # Checking for valid email address
    def is_valid_email(self, email):
        email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
        return email_pattern.match(email)
    
    # Using regular expressions to check for strong password criteria
    def is_strong_password(self, password):
        length_check = len(password) >= 8
        uppercase_check = re.search(r"[A-Z]", password)
        lowercase_check = re.search(r"[a-z]", password)
        digit_check = re.search(r"\d", password)
        special_char_check = re.search(r"[\W_]", password)
        
        return length_check and uppercase_check and lowercase_check and digit_check and special_char_check

    # Updating the live video feed
    def update_video_feed(self, label):
        _, frame = self.security_system.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image=image)
        label.imgtk = photo
        label.configure(image=photo)
        label.after(10, lambda: self.update_video_feed(label))

    # Open Live View
    def open_live_view(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = Frame(self.root, bg=BG_COLOUR)
        self.current_screen.pack(fill=BOTH, expand=True)

        self.video_feed_label = Label(self.current_screen, bg=BG_COLOUR)
        self.video_feed_label.pack()

        self.update_video_feed(self.video_feed_label)

        self.back_button = ttk.Button(self.current_screen, text="Back", command=self.create_main_menu_screen, style="TButton", width=15, cursor="hand2")
        self.back_button.pack(pady=5)
    
    # Checking and Creating Description Files
    def check_and_create_description_files(self):
        activity_files = os.listdir(self.security_system.activity_folder) # Directory

        for file in activity_files: # Iterating through files
            if file.endswith(".mp4"): # If ".mp4" video file
                recording_time = file[:-4]  # Remove ".mp4" extension
                recording_text_file = f"{recording_time}.txt"
                text_file_path = os.path.join(self.security_system.activity_folder, recording_text_file)

                if not os.path.exists(text_file_path): # If path does not exist
                    # Create and populate the text description file
                    with open(text_file_path, "w") as text_file:
                        text_file.write("Description:")

    # Open Activity Log Screen
    def open_activity_log(self):
        if self.current_screen:
            self.current_screen.destroy()
        
        self.create_activity_log_screen()

    # Creating Activity Log Screen (actual content)
    def create_activity_log_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = Frame(self.root, bg=BG_COLOUR)
        self.current_screen.pack(fill=BOTH, expand=True)

        Label(self.current_screen, text="Activity Log", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR).pack(pady=10)

        self.check_and_create_description_files() # Check and create text description files

        activity_files = os.listdir(self.security_system.activity_folder)

        # Scrollbar
        scrollbar = Scrollbar(self.current_screen)
        scrollbar.pack(side=RIGHT, fill=Y)

        canvas = Canvas(self.current_screen, yscrollcommand=scrollbar.set, bg=BG_COLOUR)
        canvas.pack(fill=BOTH, expand=True)

        scrollbar.config(command=canvas.yview)

        inner_frame = Frame(canvas, bg=BG_COLOUR)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        inner_frame.bind("<Configure>", lambda event, canvas=canvas: self.on_frame_configure(canvas))

        for file in activity_files: # Iterate through all files in folder
            if file.endswith(".mp4"): # If ".mp4" video file
                recording_time = file[:-4]  # Remove ".mp4" extension
                recording_text_file = f"{recording_time}.txt" # Select file
                text_file_path = os.path.join(self.security_system.activity_folder, recording_text_file) # Select path

                if os.path.exists(text_file_path):
                    recording_description, timestamp, metadata = self.read_description_file(text_file_path)

                    recording_label = Label(inner_frame, text=f"Recording: {recording_time}", font=(MAIN_FONT, 12), bg=BG_COLOUR, fg=FG_COLOUR)
                    recording_label.pack(padx=10, pady=5, anchor=W)

                    description_label = Label(inner_frame, text=f"Description: {recording_description}", bg=BG_COLOUR, fg=FG_COLOUR)
                    description_label.pack(padx=10, pady=2, anchor=W)

                    timestamp_label = Label(inner_frame, text=f"Timestamp: {timestamp}", bg=BG_COLOUR, fg=FG_COLOUR)
                    timestamp_label.pack(padx=10, pady=2, anchor=W)

                    metadata_label = Label(inner_frame, text=f"Edited by: {metadata}", bg=BG_COLOUR, fg=FG_COLOUR)
                    metadata_label.pack(padx=10, pady=2, anchor=W)

                    edit_button = ttk.Button(inner_frame, text="Edit Description", command=lambda path=text_file_path: self.edit_description(path), style="TButton", cursor="hand2")
                    edit_button.pack(padx=10, pady=2, anchor=W)

        # Back Button
        back_button = ttk.Button(self.current_screen, text="Back", command=self.create_main_menu_screen, style="TButton", width=15, cursor="hand2")
        back_button.pack(pady=10)

        # Update Scrollregion
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def on_frame_configure(self, canvas):
        canvas.config(scrollregion=canvas.bbox("all"))

    # Reading Description Files
    def read_description_file(self, text_file_path):
        recording_description = ""
        timestamp = ""
        metadata = ""

        with open(text_file_path, "r") as text_file:
            lines = text_file.readlines()

            if lines:
                recording_description = lines[0].strip()
                if len(lines) >= 2:
                    timestamp = lines[1].strip()
                if len(lines) >= 3:
                    metadata = lines[2].strip()

        return recording_description, timestamp, metadata
    
    # Editing Description Files
    def edit_description(self, text_file_path):
        self.edit_description_window = Toplevel(self.root)
        self.edit_description_window.title("Edit Description")
        self.edit_description_window.config(bg=BG_COLOUR)  # Set background color of the window

        description_text, timestamp, metadata = self.read_description_file(text_file_path)

        description_label = Label(self.edit_description_window, text="Edit Description:", font=(MAIN_FONT, 14), bg=BG_COLOUR, fg=FG_COLOUR)
        description_label.pack(pady=10)

        description_entry = Text(self.edit_description_window, wrap=WORD, font=(MAIN_FONT, 12), width=40, height=10, bg=BG_COLOUR, fg=FG_COLOUR)
        description_entry.insert("1.0", description_text)
        description_entry.pack(padx=10, pady=5)

        save_button = ttk.Button(self.edit_description_window, text="Save", command=lambda: self.save_description(description_entry.get("1.0", "end-1c"), text_file_path), style="TButton")
        save_button.pack(pady=10)
    
    # Saving Edited Descriptions
    def save_description(self, description, text_file_path):
        with open(text_file_path, "w") as file:
            file.write(description)
        self.edit_description_window.destroy()
        self.create_activity_log_screen()  # Refresh Activity Log Window
    
    # Updating Description Preview
    def update_description(self, description_text, text_file_path):
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        username = self.username_entry.get()  # REPLACE WITH ACTUAL USERNAME
        metadata = f"{username} ({timestamp})"

        with open(text_file_path, "w") as text_file:
            text_file.write(f"{description_text}\n")
            text_file.write(f"Original Timestamp: {timestamp}\n")
            text_file.write(f"Edited by: {metadata}\n")

    # Open Print Report
    def open_print_report(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.create_print_report_screen()
    
    # Create Print Report Screen
    def create_print_report_screen(self):
        if self.current_screen:
            self.current_screen.destroy()

        self.current_screen = Frame(self.root, bg=BG_COLOUR)
        self.current_screen.pack(fill=BOTH, expand=True)

        Label(self.current_screen, text="Print Report", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR).pack(pady=10)

        activity_files = os.listdir(self.security_system.activity_folder)
        recording_options = []

        # Iterate through ".mp4" video files in the selected path
        for file in activity_files:
            if file.endswith(".mp4"):
                recording_time = file[:-4]  # Remove ".mp4" extension
                recording_text_file = f"{recording_time}.txt"
                recording_options.append((recording_text_file, recording_time))

        self.selected_recording = StringVar()
        self.selected_recording.set(recording_options[0][0])

        # Title
        recording_label = Label(self.current_screen, text="Select Recording:", font=(MAIN_FONT, 12), bg=BG_COLOUR, fg=FG_COLOUR)
        recording_label.pack(padx=10, pady=5, anchor=W)

        recording_menu = ttk.OptionMenu(self.current_screen, self.selected_recording, recording_options[0][0], *[option[0] for option in recording_options])
        recording_menu.pack(fill=X, padx=10, pady=5)

        # Print Button
        print_button = ttk.Button(self.current_screen, text="Print", command=self.print_selected_recording, style="TButton", width=15, cursor="hand2")
        print_button.pack(pady=10)

        # Back Button
        self.back_button = ttk.Button(self.current_screen, text="Back", command=self.create_main_menu_screen, style="TButton", width=15, cursor="hand2")
        self.back_button.pack(pady=10)

    # Print Recording Descriptions - Logic
    def print_selected_recording(self):
        selected_recording = self.selected_recording.get()
        text_file_path = os.path.join(self.security_system.activity_folder, selected_recording)

        try:
            if os.path.exists(text_file_path):
                with open(text_file_path, "r") as file:
                    text_content = file.read()

                    # Print content to the default printer
                    printer_name = win32print.GetDefaultPrinter()
                    if not printer_name:
                        messagebox.showerror("Printer Error", "No printer found. Please set up a printer.")
                        return

                    hprinter = win32print.OpenPrinter(printer_name)
                    try:
                        printer_info = win32print.GetPrinter(hprinter, 2)
                        if win32print.StartDocPrinter(hprinter, 1, ("Document", None, "RAW")):
                            win32print.StartPagePrinter(hprinter)
                            win32print.WritePrinter(hprinter, text_content.encode())
                            win32print.EndPagePrinter(hprinter)
                            win32print.EndDocPrinter(hprinter)
                    finally:
                        win32print.ClosePrinter(hprinter)
            else:
                messagebox.showerror("Error", "Selected recording not found.")
        except pywintypes.error as e:
            error_message = e.args[2]
            messagebox.showerror("Printer Error", f"An error occurred while accessing the printer: {error_message}")

    # Toggling Security System
    def toggle_security_system(self):
        if self.security_system.security_system_active:
            self.security_system.stop_security_system()
            self.security_button_text.set("Turn On Security System")
        else:
            self.security_system.start_security_system()
            self.security_button_text.set("Turn Off Security System")

    # Registration Logic
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

    # Confirm User Deletion
    def delete_user_confirm(self):
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if response:
            self.delete_user()

    # Confirm Program Exit
    def exit_program(self):
        self.security_system.release_camera()
        self.root.destroy()

# -------- Main Loop --------
if __name__ == "__main__":
    root = Tk()
    root.config(bg=BG_COLOUR)
    app = App(root)

    # Confirm program exit and releasing resources
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if app.security_system.security_system_active:
                app.security_system.release_camera()
            app.exit_program()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()