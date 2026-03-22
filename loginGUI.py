import customtkinter as ctk
import requests
import subprocess
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("390x844")
        self.title("Seekseven")
        self.configure(fg_color="#0f172a")

        self.signup = SignupFrame(self)
        self.login = LoginFrame(self)

        self.show_login()

    def show_login(self):
        self.signup.pack_forget()
        self.login.pack(fill="both", expand=True)

    def show_signup(self):
        self.login.pack_forget()
        self.signup.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.destroy()
        subprocess.Popen([sys.executable, "mytk.py"])


class SignupFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0f172a")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(container, text="Create Account",
                     font=("Arial", 26, "bold")).pack(pady=(0, 6))

        ctk.CTkLabel(container, text="Sign up to get started",
                     text_color="#94a3b8").pack(pady=(0, 18))

        self.name = ctk.CTkEntry(container, placeholder_text="Full Name", width=300)
        self.name.pack(pady=6)

        self.email = ctk.CTkEntry(container, placeholder_text="Email", width=300)
        self.email.pack(pady=6)

        self.password = ctk.CTkEntry(container, placeholder_text="Password", show="*", width=300)
        self.password.pack(pady=6)

        self.confirm = ctk.CTkEntry(container, placeholder_text="Confirm Password", show="*", width=300)
        self.confirm.pack(pady=6)

        self.message = ctk.CTkLabel(container, text="", text_color="red")
        self.message.pack(pady=5)

        ctk.CTkButton(container, text="Sign Up", width=300,
                      command=self.signup).pack(pady=10)

        link = ctk.CTkLabel(container, text="Already have an account? Log in",
                            text_color="#3b82f6", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: master.show_login())

    def signup(self):
        name = self.name.get()
        email = self.email.get()
        pwd = self.password.get()
        confirm = self.confirm.get()

        if not name or not email or not pwd or not confirm:
            self.message.configure(text="All fields required")
            return

        if pwd != confirm:
            self.message.configure(text="Passwords do not match")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/register",
                data={
                    "fullname": name,
                    "email": email,
                    "password": pwd
                }
            )

            result = response.text.strip()

            if result == "success":
                self.message.configure(text="Account created", text_color="green")

            elif result == "exists":
                self.message.configure(text="Email already exists")

            elif result == "empty":
                self.message.configure(text="All fields required")

            else:
                self.message.configure(text="Signup failed")

        except:
            self.message.configure(text="Server not running")


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0f172a")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(container, text="Welcome Back",
                     font=("Arial", 26, "bold")).pack(pady=5)

        ctk.CTkLabel(container, text="Login to your account",
                     text_color="#94a3b8").pack(pady=5)

        self.email = ctk.CTkEntry(container, placeholder_text="Email", width=300)
        self.email.pack(pady=6)

        self.password = ctk.CTkEntry(container, placeholder_text="Password", show="*", width=300)
        self.password.pack(pady=6)

        self.message = ctk.CTkLabel(container, text="", text_color="red")
        self.message.pack(pady=5)

        ctk.CTkButton(container, text="Login", width=300,
                      command=self.login).pack(pady=10)

        link = ctk.CTkLabel(container, text="Create account",
                            text_color="#3b82f6", cursor="hand2")
        link.pack()
        link.bind("<Button-1>", lambda e: master.show_signup())

    def login(self):
        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                data={
                    "email": self.email.get(),
                    "password": self.password.get()
                }
            )

            result = response.text.strip()

            if result == "success":
                self.master.show_dashboard()

            elif result == "no_user":
                self.message.configure(text="User not found")

            elif result == "wrong_password":
                self.message.configure(text="Incorrect password")

            else:
                self.message.configure(text="Login failed")

        except:
            self.message.configure(text="Server not running")


if __name__ == "__main__":
    app = App()
    app.mainloop()