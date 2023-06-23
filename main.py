from tkinter import *
from tkinter import ttk
import tkinter.messagebox as messagebox

# Define the color scheme for the dark theme
BG_COLOR = "#424242"
FG_COLOR = "#F1F2F6"
TITLE_COLOR = "#FB3640"
ENTRY_BG_COLOR = "#424242"
ENTRY_FG_COLOR = "#F1F2F6"
BUTTON_BG_COLOR = "#424242"
BUTTON_FG_COLOR = "#23967F"
MAIN_FONT = "Impact"
BUTTON_RADIUS = 20  # Radius for rounded edges of buttons
ENTRY_RADIUS = 20  # Radius for rounded edges of entry fields

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("400x250")  # Set window size
        
        self.root.config(bg=BG_COLOR)  # Set background color
        
        style = ttk.Style()
        style.configure("TButton", background=BUTTON_BG_COLOR, foreground=BUTTON_FG_COLOR, font=(MAIN_FONT, 10), relief="flat", borderwidth=0)
        style.map("TButton", background=[("active", "#555555")])

        self.login_label = Label(root, text = "LOGIN", font=(MAIN_FONT, 20), bg=BG_COLOR, fg=TITLE_COLOR)
        self.login_label.pack()
        
        self.username_label = Label(root, text="Username:", font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
        self.username_label.pack()
        
        self.username_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOR, background=ENTRY_BG_COLOR)
        self.username_entry.pack(pady=5)  # Add vertical padding
        
        self.password_label = Label(root, text="Password:", font=(MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
        self.password_label.pack()
        
        self.password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOR, background=ENTRY_BG_COLOR)
        self.password_entry.pack(pady=5)  # Add vertical padding
        
        self.login_button = ttk.Button(root, text="Log In", command=self.login, style="TButton", width=15, cursor="hand2")
        self.login_button.pack(pady=10)  # Add vertical padding
        
        self.register_button = ttk.Button(root, text="Register", command=self.open_registration, style="TButton", width=15, cursor="hand2")
        self.register_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        with open("users.txt", "r") as file:
            for line in file:
                user_info = line.strip().split(",")
                if len(user_info) == 3:
                    saved_username, saved_password = user_info[1], user_info[2]
                    if username == saved_username and password == saved_password:
                        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
                        self.root.destroy()  # Close the login window
                        self.open_dashboard()
                        return
        
        messagebox.showerror("Login Failed", "Invalid username or password")

    def open_registration(self):
        self.root.withdraw()  # Hide the login window
        registration_window = Toplevel(self.root)
        registration_window.title("Registration")
        registration_window.geometry("350x250")  # Set window size
        registration_window.config(bg=BG_COLOR)  # Set background color
        registration = RegistrationWindow(registration_window, self.root)
        registration_window.protocol("WM_DELETE_WINDOW", lambda: self.back(registration_window))

    def open_dashboard(self):
        dashboard_window = Tk()
        dashboard_window.title("Dashboard")
        dashboard_window.geometry("400x300")  # Set window size
        dashboard_window.config(bg=BG_COLOR)  # Set background color
        # Add your dashboard code here
        dashboard_window.mainloop()

    def back(self, window):
        window.destroy()
        self.root.deiconify()


class RegistrationWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.geometry("350x425")  # Set window size
        self.root.title("Registration")
        self.root.config(bg=BG_COLOR)  # Set background color

        style = ttk.Style()
        style.configure("TEntry", fieldbackground=ENTRY_BG_COLOR, foreground=ENTRY_FG_COLOR, bordercolor=BUTTON_BG_COLOR, borderwidth=0, focuscolor=BUTTON_BG_COLOR)
        style.map("TEntry", background=[("active", ENTRY_BG_COLOR)], relief=[("focus", "flat")])

        self.registration_label = Label(root, text = "REGISTRATION", font = (MAIN_FONT, 20), bg = BG_COLOR, fg = TITLE_COLOR)
        self.registration_label.pack()

        self.email_label = Label(root, text="Email:", font = (MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
        self.email_label.pack()

        self.email_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOR, background=ENTRY_BG_COLOR)
        self.email_entry.pack(pady=5)  # Add vertical padding

        self.username_label = Label(root, text="Username:", font = (MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
        self.username_label.pack()

        self.username_entry = ttk.Entry(root, style="TEntry", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOR, background=ENTRY_BG_COLOR)
        self.username_entry.pack(pady=5)  # Add vertical padding

        self.password_label = Label(root, text="Password:", font = (MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
        self.password_label.pack()

        self.password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOR, background=ENTRY_BG_COLOR)
        self.password_entry.pack(pady=5)  # Add vertical padding

        self.confirm_password_label = Label(root, text="Confirm Password:", font = (MAIN_FONT, 10), bg=BG_COLOR, fg=FG_COLOR)
        self.confirm_password_label.pack()

        self.confirm_password_entry = ttk.Entry(root, style="TEntry", show="*", width=20, font=(MAIN_FONT, 10), foreground=ENTRY_FG_COLOR, background=ENTRY_BG_COLOR)
        self.confirm_password_entry.pack(pady=5)  # Add vertical padding

        self.blank_line = Label(root, text="", bg=BG_COLOR, fg=FG_COLOR) # BLANK LINE
        self.blank_line.pack() # BLANK LINE

        self.register_button = ttk.Button(root, text="Register", command=self.register, style="TButton", width=15, cursor="hand2")
        self.register_button.pack(pady=5)  # Add vertical padding

        self.delete_button = ttk.Button(root, text="Delete User", command=self.delete_user, style="TButton", width=15, cursor="hand2")
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
            with open("users.txt", "a") as file:
                file.write(f"{email},{username},{password}\n")

            messagebox.showinfo("Registration Successful", "You have been registered successfully")
            self.clear_fields()

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
        self.root.destroy()
        self.login_window.deiconify()

    def clear_fields(self):
        self.email_entry.delete(0, END)
        self.username_entry.delete(0, END)
        self.password_entry.delete(0, END)
        self.confirm_password_entry.delete(0, END)


if __name__ == "__main__":
    root = Tk()
    root.config(bg = BG_COLOR)  # Set background color
    login = LoginWindow(root)
    root.mainloop()
