import customtkinter as ctk
import requests
from mytk import App as DashboardApp  # 🔥 IMPORT YOUR REAL DASHBOARD


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


        self.show_signup()


    def show_signup(self):
        self.login.pack_forget()
        self.signup.pack(fill="both", expand=True)


    def show_login(self):
        self.signup.pack_forget()
        self.login.pack(fill="both", expand=True)


    # 🔥 REAL DASHBOARD REDIRECT
    def show_dashboard(self):
        self.destroy()  # close login window


        dashboard = DashboardApp()
        dashboard.mainloop()




# ---------------- SIGNUP ----------------
class SignupFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0f172a")


        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.45, anchor="center")


        ctk.CTkLabel(container, text="Create Account",
                     font=("Arial", 26, "bold")).pack(pady=(0, 6))


        ctk.CTkLabel(container, text="Sign up to get started",
                     text_color="#94a3b8",
                     font=("Arial", 13)).pack(pady=(0, 18))


        entry_style = {
            "height": 42,
            "corner_radius": 14,
            "fg_color": "#1e293b",
            "border_width": 0,
            "font": ("Arial", 13)
        }


        width = 300


        self.name = ctk.CTkEntry(container, placeholder_text="Full Name", width=width, **entry_style)
        self.name.pack(pady=6)


        self.email = ctk.CTkEntry(container, placeholder_text="Email", width=width, **entry_style)
        self.email.pack(pady=6)


        self.password = ctk.CTkEntry(container, placeholder_text="Password", show="*", width=width, **entry_style)
        self.password.pack(pady=6)


        self.confirm = ctk.CTkEntry(container, placeholder_text="Confirm Password", show="*", width=width, **entry_style)
        self.confirm.pack(pady=6)


        self.message = ctk.CTkLabel(container, text="", text_color="red", font=("Arial", 12))
        self.message.pack(pady=(4, 6))


        self.switch = ctk.CTkSwitch(container, text="Show Password", command=self.toggle_password)
        self.switch.pack(pady=(6, 10))


        ctk.CTkButton(
            container,
            text="Sign Up",
            width=300,
            height=44,
            corner_radius=20,
            fg_color="#ff6b4a",
            hover_color="#ff5a36",
            font=("Arial", 14, "bold"),
            command=self.signup
        ).pack(pady=(10, 10))


        link = ctk.CTkLabel(
            container,
            text="Already have an account? Log in",
            text_color="#3b82f6",
            font=("Arial", 12),
            cursor="hand2"
        )
        link.pack()


        link.bind("<Button-1>", lambda e: master.show_login())


    def toggle_password(self):
        show = "" if self.switch.get() else "*"
        self.password.configure(show=show)
        self.confirm.configure(show=show)


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


        if len(pwd) < 6:
            self.message.configure(text="Password must be at least 6 characters")
            return


        try:
            response = requests.post(
                "http://localhost/register.php",
                data={"fullname": name, "email": email, "password": pwd},
                timeout=5
            )


            result = response.text.strip()


            if result == "success":
                self.message.configure(text="Account created!", text_color="green")


            elif result == "exists":
                self.message.configure(text="Email already exists")


            else:
                self.message.configure(text="Server error")


        except:
            self.message.configure(text="Server not running")




# ---------------- LOGIN ----------------
class LoginFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#0f172a")


        self.master = master


        container = ctk.CTkFrame(self, fg_color="transparent")
        container.place(relx=0.5, rely=0.45, anchor="center")


        ctk.CTkLabel(container, text="Welcome Back",
                     font=("Arial", 26, "bold")).pack(pady=(0, 6))


        ctk.CTkLabel(container, text="Login to your account",
                     text_color="#94a3b8",
                     font=("Arial", 13)).pack(pady=(0, 18))


        width = 300


        self.email = ctk.CTkEntry(container, placeholder_text="Email", width=width)
        self.email.pack(pady=6)


        self.password = ctk.CTkEntry(container, placeholder_text="Password", show="*", width=width)
        self.password.pack(pady=6)


        self.message = ctk.CTkLabel(container, text="", text_color="red")
        self.message.pack(pady=6)


        ctk.CTkButton(
            container,
            text="Log In",
            width=300,
            height=44,
            fg_color="#3b82f6",
            command=self.login
        ).pack(pady=10)


        link = ctk.CTkLabel(
            container,
            text="Create an account",
            text_color="#3b82f6",
            cursor="hand2"
        )
        link.pack()


        link.bind("<Button-1>", lambda e: master.show_signup())


    def login(self):
        email = self.email.get()
        pwd = self.password.get()


        if not email or not pwd:
            self.message.configure(text="All fields required")
            return


        try:
            response = requests.post(
                "http://localhost/login.php",
                data={"email": email, "password": pwd},
                timeout=5
            )


            result = response.text.strip()


            if result == "success":
                self.message.configure(text="Login success", text_color="green")
                self.master.show_dashboard()  # 🔥 OPEN REAL DASHBOARD


            elif result == "notfound":
                self.message.configure(text="User not found")


            elif result == "wrong":
                self.message.configure(text="Wrong password")


            else:
                self.message.configure(text="Server error")


        except:
            self.message.configure(text="Server not running")




if __name__ == "__main__":
    app = App()
    app.mainloop()

