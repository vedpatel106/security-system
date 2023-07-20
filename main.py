from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox

# Define the COLOUR scheme for the dark theme
BG_COLOUR = "#424242"
FG_COLOUR = "#F1F2F6"
TITLE_COLOUR = "#FB3640"
ENTRY_BG_COLOUR = "#424242"
ENTRY_FG_COLOUR = "#424242"
BUTTON_BG_COLOUR = "#424242"
BUTTON_FG_COLOUR = "#23967F"
MAIN_FONT = "Impact"
BUTTON_RADIUS = 20  # Radius for rounded edges of buttons
ENTRY_RADIUS = 20  # Radius for rounded edges of entry fields

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")  # Set window size
        
        self.root.config(bg=BG_COLOUR)  # Set background colour
        
        style = ttk.Style()
        style.configure("TButton", background=BUTTON_BG_COLOUR, foreground=BUTTON_FG_COLOUR, font=(MAIN_FONT, 10), relief="flat", borderwidth=0)
        style.map("TButton", background=[("active", "#555555")], foreground=[("active", BUTTON_BG_COLOUR)])

        self.login_label = Label(root, text = "LOGIN", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.login_label.pack()
        
        self.username_label = Label(root, text="Username:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.username_label.pack()
        
        self.username_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.username_entry.pack(pady=5)  # Add vertical padding
        
        self.password_label = Label(root, text="Password:", font=(MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.password_label.pack()
        
        self.password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.password_entry.pack(pady=5)  # Add vertical padding
        
        self.login_button = ttk.Button(root, text="Log In", command=self.login, style="TButton", width=15, cursor="hand2")
        self.login_button.pack(pady=10)  # Add vertical padding
        
        self.register_button = ttk.Button(root, text="Register", command=self.open_registration, style="TButton", width=15, cursor="hand2")
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        with open("users.csv", "r") as file:
            for line in file:
                user_info = line.strip().split(",")
                if len(user_info) == 3:
                    saved_username, saved_password = user_info[1], user_info[2]
                    if username == saved_username and password == saved_password:
                        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                        self.root.withdraw()  # Hide the login window
                        main_menu_window = Toplevel(self.root)
                        MainMenuWindow(main_menu_window, self)
                        return
        
        messagebox.showerror("Login Failed", "Invalid username or password")

    def open_registration(self):
        self.root.withdraw()  # Hide the login window
        registration_window = Toplevel(self.root)
        RegistrationWindow(registration_window, self.root)
        registration_window.protocol("WM_DELETE_WINDOW", lambda: self.back(registration_window))

    def back(self, window):
        window.destroy()
        self.root.deiconify()


class RegistrationWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.geometry("350x425")  # Set window size
        self.root.title("Registration")
        self.root.config(bg=BG_COLOUR)  # Set background colour

        style = ttk.Style()
        style.configure("TEntry", fieldbackground=ENTRY_BG_COLOUR, foreground=ENTRY_FG_COLOUR, bordercolour=BUTTON_BG_COLOUR, borderwidth=0, focuscolour=BUTTON_BG_COLOUR)
        style.map("TEntry", background=[("active", ENTRY_BG_COLOUR)], relief=[("focus", "flat")])

        self.registration_label = Label(root, text = "REGISTRATION", font = (MAIN_FONT, 20), bg = BG_COLOUR, fg = TITLE_COLOUR)
        self.registration_label.pack()

        self.email_label = Label(root, text="Email:", font = (MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.email_label.pack()

        self.email_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.email_entry.pack(pady=5)  # Add vertical padding

        self.username_label = Label(root, text="Username:", font = (MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.username_label.pack()

        self.username_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.username_entry.pack(pady=5)  # Add vertical padding

        self.password_label = Label(root, text="Password:", font = (MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.password_label.pack()

        self.password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.password_entry.pack(pady=5)  # Add vertical padding

        self.confirm_password_label = Label(root, text="Confirm Password:", font = (MAIN_FONT, 10), bg=BG_COLOUR, fg=FG_COLOUR)
        self.confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOUR, background=ENTRY_BG_COLOUR)
        self.confirm_password_entry.pack(pady=5)  # Add vertical padding

        self.blank_line = Label(root, text="", bg=BG_COLOUR, fg=FG_COLOUR) # BLANK LINE
        self.blank_line.pack() # BLANK LINE

        self.register_button = ttk.Button(root, text="Register", command=self.register, style="TButton", width=15, cursor="hand2")
        self.register_button.pack(pady=5)  # Add vertical padding

        self.delete_button = ttk.Button(root, text="Delete User", command=self.delete_user_confirm, style="TButton", width=15, cursor="hand2")
        self.delete_button.pack(pady=5) # Add vertical padding

        self.back_button = ttk.Button(root, text="Back", command=self.back, style="TButton", width=15, cursor="hand2")
        self.back_button.pack(pady=5) # Add vertical padding

    def register(self):
        email = self.email_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not (email and username and password and confirm_password):
            messagebox.showerror("Error", "Please fill in all fields")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            with open("users.csv", "a") as file:
                file.write(f"{email},{username},{password}\n")

            messagebox.showinfo("Registration Successful", "You have been registered successfully")
            self.clear_fields()

    def delete_user_confirm(self):
        response = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this user?")
        if response:
            self.delete_user()

    def delete_user(self):
        username = self.username_entry.get()
        lines = []

        with open("users.txt", "r") as file:
            for line in file:
                user_info = line.strip().split(",")
                if len(user_info) == 3:
                    saved_username = user_info[1]
                    if username != saved_username:
                        lines.append(line)

        with open("users.txt", "w") as file:
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


class MainMenuWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.geometry("400x250")  # Set window size
        self.root.title("Main Menu")
        self.root.config(bg=BG_COLOUR)  # Set background colour

        self.title_label = Label(root, text="Main Menu", font=(MAIN_FONT, 20), bg=BG_COLOUR, fg=TITLE_COLOUR)
        self.title_label.pack(pady=10)

        self.live_view_button = ttk.Button(root, text="Live View", command=self.open_live_view, style="TButton", width=15,
                                           cursor="hand2")
        self.live_view_button.pack(pady=5)

        self.activity_log_button = ttk.Button(root, text="View Activity Log", command=self.open_activity_log,
                                              style="TButton", width=20, cursor="hand2")
        self.activity_log_button.pack(pady=5)

        self.print_report_button = ttk.Button(root, text="Print Report", command=self.open_print_report,
                                              style="TButton", width=15, cursor="hand2")
        self.print_report_button.pack(pady=5)

        self.exit_button = ttk.Button(root, text="Exit", command=self.root.quit, style="TButton", width=15, cursor="hand2")
        self.exit_button.pack(pady=5)

    def open_live_view(self):
        live_view_window = Toplevel(self.root)
        live_view_window.title("Live View")
        live_view_window.geometry("400x200")
        live_view_window.config(bg=BG_COLOUR)
        Label(live_view_window, text="This is the Live View window", font=(MAIN_FONT, 14), bg=BG_COLOUR, fg=FG_COLOUR).pack(pady=30)

    def open_activity_log(self):
        activity_log_window = Toplevel(self.root)
        activity_log_window.title("Activity Log")
        activity_log_window.geometry("400x200")
        activity_log_window.config(bg=BG_COLOUR)
        Label(activity_log_window, text="This is the Activity Log window", font=(MAIN_FONT, 14), bg=BG_COLOUR, fg=FG_COLOUR).pack(pady=30)

    def open_print_report(self):
        print_report_window = Toplevel(self.root)
        print_report_window.title("Print Report")
        print_report_window.geometry("400x200")
        print_report_window.config(bg=BG_COLOUR)
        Label(print_report_window, text="This is the Print Report window", font=(MAIN_FONT, 14), bg=BG_COLOUR, fg=FG_COLOUR).pack(pady=30)


if __name__ == "__main__":
    root = Tk()
    root.config(bg=BG_COLOUR)  # Set background colour
    login_window = LoginWindow(root)

    root.mainloop()
