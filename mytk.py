import customtkinter as ctk
from urllib.request import urlopen
import json
import pandas as pd
from PIL import Image

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

LITERS_PER_BARREL = 158.98
VAT_RATE = 0.12


def get_prices():
    try:
        url = 'https://www.floatrates.com/daily/usd.json'
        data = json.loads(urlopen(url).read())
        rate = data['php']['rate']

        df = pd.read_csv("crude_oil_brent.csv", parse_dates=["Date"])
        latest = df.loc[df["Date"].idxmax()]["Price"]

        base = (latest / LITERS_PER_BARREL) * rate

        return {
            "Unleaded": round((base + 15 + 9 + 10) * (1 + VAT_RATE), 2),
            "Premium": round((base + 15 + 9 + 10 + 2) * (1 + VAT_RATE), 2),
            "Diesel": round((base + 15 + (9+25) + 6) * (1 + VAT_RATE), 2)
        }
    except:
        return {
            "Unleaded": 77.94,
            "Premium": 80.18,
            "Diesel": 101.46
        }


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("1000x650")
        self.title("Seekseven")

        self.sidebar_visible = True
        self.dark_mode = ctk.StringVar(value="Light")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=200, fg_color="#13389D")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # MAIN
        self.main = ctk.CTkFrame(self, fg_color="#f3f4f6")
        self.main.grid(row=0, column=1, sticky="nsew")

        ctk.CTkButton(
            self.main,
            text="☰",
            width=40,
            fg_color="transparent",
            command=self.toggle_sidebar
        ).pack(anchor="nw", padx=10, pady=10)

        self.title_label = ctk.CTkLabel(
            self.main,
            text="Fuel Pump",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(anchor="nw", padx=60, pady=10)

        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_sidebar()
        self.show_page("Fuel Pump")

    def build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Seekseven", text_color="white").pack(pady=15)

        for item in ["Dashboard", "Delivery Schedule", "Fuel Pump", "Settings"]:
            ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                text_color="white",
                command=lambda b=item: self.change_page(b)
            ).pack(fill="x", padx=20, pady=5)

        self.side_toggle = ctk.CTkButton(
            self.sidebar,
            text="❮",
            width=20,
            height=40,
            fg_color="transparent",
            text_color="white",
            command=self.toggle_sidebar
        )
        self.side_toggle.place(relx=1.0, rely=0.5, anchor="e")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.grid_remove()
            self.sidebar_visible = False
        else:
            self.sidebar.grid()
            self.sidebar_visible = True

    def change_page(self, name):
        self.show_page(name)

    def show_page(self, name):
        for w in self.content.winfo_children():
            w.destroy()

        if name == "Fuel Pump":
            self.create_fuel_page().pack(fill="both", expand=True)
        elif name == "Dashboard":
            self.create_dashboard_page().pack(fill="both", expand=True)
        elif name == "Delivery Schedule":
            self.create_delivery_page().pack(fill="both", expand=True)
        elif name == "Settings":
            self.create_settings_page().pack(fill="both", expand=True)

    # DASHBOARD
    def create_dashboard_page(self):
        frame = ctk.CTkFrame(self.content)
        ctk.CTkLabel(frame, text="Dashboard", font=("Arial", 24, "bold")).pack(pady=40)
        ctk.CTkLabel(frame, text="Welcome to your dashboard").pack()
        return frame

    # DELIVERY SCHEDULE (WORKING)
    def create_delivery_page(self):
        frame = ctk.CTkFrame(self.content)

        ctk.CTkLabel(frame, text="Delivery Schedule", font=("Arial", 24, "bold")).pack(pady=20)

        date_entry = ctk.CTkEntry(frame, placeholder_text="Enter date (YYYY-MM-DD)")
        date_entry.pack(pady=10)

        schedule_list = ctk.CTkTextbox(frame, height=200, width=300)
        schedule_list.pack(pady=10)
        schedule_list.insert("end", "No schedules yet\n")

        schedules = []

        def add_schedule():
            date = date_entry.get()
            if date.strip() == "":
                return

            schedules.append(date)

            schedule_list.delete("1.0", "end")
            for i, d in enumerate(schedules, 1):
                schedule_list.insert("end", f"{i}. {d}\n")

            date_entry.delete(0, "end")

        def remove_schedule():
            if schedules:
                schedules.pop()
                schedule_list.delete("1.0", "end")

                if schedules:
                    for i, d in enumerate(schedules, 1):
                        schedule_list.insert("end", f"{i}. {d}\n")
                else:
                    schedule_list.insert("end", "No schedules yet\n")

        ctk.CTkButton(frame, text="Add Schedule", command=add_schedule).pack(pady=5)
        ctk.CTkButton(frame, text="Remove Last", command=remove_schedule).pack(pady=5)

        return frame

    # SETTINGS
    def create_settings_page(self):
        frame = ctk.CTkFrame(self.content)

        ctk.CTkLabel(frame, text="Settings", font=("Arial", 24, "bold")).pack(pady=20)
        ctk.CTkLabel(frame, text="Appearance Mode").pack(pady=10)

        mode_menu = ctk.CTkOptionMenu(
            frame,
            values=["Light", "Dark"],
            variable=self.dark_mode,
            command=self.change_appearance
        )
        mode_menu.pack(pady=10)

        return frame

    def change_appearance(self, mode):
        ctk.set_appearance_mode("dark" if mode == "Dark" else "light")

    # FUEL PAGE
    def create_fuel_page(self):
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        frame.grid_columnconfigure(0, weight=2)
        frame.grid_columnconfigure(1, weight=1)

        data = get_prices()

        # LEFT
        left = ctk.CTkFrame(frame, fg_color="#e5e7eb")
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(left, text="Vehicle Preview", font=("Arial", 16, "bold")).pack(pady=10)

        vehicle_display = ctk.CTkLabel(left, text="Sedan", font=("Arial", 18, "bold"))
        vehicle_display.pack(pady=10)

        preview = ctk.CTkFrame(left, height=200, fg_color="white")
        preview.pack(fill="x", padx=20, pady=10)

        self.vehicle_images = {
            "Motorcycle": ctk.CTkImage(Image.open("assets/MOTOR.jpg"), size=(220, 140)),
            "Sedan": ctk.CTkImage(Image.open("assets/SEDAN.jpg"), size=(220, 140)),
            "SUV": ctk.CTkImage(Image.open("assets/CAR.jpg"), size=(220, 140)),
            "Truck": ctk.CTkImage(Image.open("assets/TRUCK.jpg"), size=(220, 140)),
        }

        preview_label = ctk.CTkLabel(preview, text="", image=self.vehicle_images["Sedan"])
        preview_label.pack(expand=True)

        vehicle_frame = ctk.CTkFrame(left, fg_color="transparent")
        vehicle_frame.pack(pady=10)

        vehicle_buttons = {}

        def select_vehicle(name):
            vehicle_display.configure(text=name)
            preview_label.configure(image=self.vehicle_images[name])
            for v, btn in vehicle_buttons.items():
                btn.configure(fg_color="#2563eb" if v == name else "gray")

        for v in ["Motorcycle", "Sedan", "SUV", "Truck"]:
            btn = ctk.CTkButton(
                vehicle_frame,
                text=v,
                width=110,
                fg_color="gray",
                command=lambda x=v: select_vehicle(x)
            )
            btn.pack(side="left", padx=5)
            vehicle_buttons[v] = btn

        select_vehicle("Sedan")

        # RIGHT
        right = ctk.CTkFrame(frame, fg_color="#f9fafb")
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        selected = ctk.StringVar(value="Unleaded")

        ctk.CTkLabel(right, text="Fuel Type").pack(pady=5)

        for fuel, price in data.items():
            ctk.CTkRadioButton(
                right,
                text=f"{fuel} ₱{price}/L",
                variable=selected,
                value=fuel
            ).pack(anchor="w", padx=10)

        entry = ctk.CTkEntry(right, placeholder_text="Enter amount (₱)")
        entry.pack(pady=10)

        display = ctk.CTkLabel(right, text="0.00 L\n₱0.00", font=("Arial", 18, "bold"))
        display.pack(pady=15)

        state = {"running": False, "liters": 0, "price": 0, "target": 0}

        self.start_btn = ctk.CTkButton(right, text="Start Pump")
        self.start_btn.pack(pady=5)

        self.stop_btn = ctk.CTkButton(right, text="Stop")
        self.stop_btn.pack(pady=5)

        self.reset_btn = ctk.CTkButton(right, text="Reset")
        self.reset_btn.pack(pady=5)

        def start():
            try:
                state["price"] = data[selected.get()]
                state["target"] = float(entry.get())
                state["liters"] = 0
                state["running"] = True

                self.start_btn.configure(fg_color="green")
                self.stop_btn.configure(fg_color="#3b82f6")
                self.reset_btn.configure(fg_color="#3b82f6")

                pump_loop()
            except:
                display.configure(text="Invalid input")

        def stop():
            state["running"] = False
            self.stop_btn.configure(fg_color="red")
            self.start_btn.configure(fg_color="#3b82f6")
            self.reset_btn.configure(fg_color="#3b82f6")

        def reset():
            state["running"] = False
            state["liters"] = 0
            display.configure(text="0.00 L\n₱0.00")

            self.reset_btn.configure(fg_color="orange")
            self.start_btn.configure(fg_color="#3b82f6")
            self.stop_btn.configure(fg_color="#3b82f6")

        self.start_btn.configure(command=start)
        self.stop_btn.configure(command=stop)
        self.reset_btn.configure(command=reset)

        def pump_loop():
            if not state["running"]:
                return

            state["liters"] += 0.05
            total = state["liters"] * state["price"]

            if total >= state["target"]:
                total = state["target"]
                state["liters"] = total / state["price"]
                state["running"] = False

            display.configure(text=f"{state['liters']:.2f} L\n₱{total:.2f}")

            if state["running"]:
                frame.after(80, pump_loop)

        return frame


if __name__ == "__main__":
    app = App()
    app.mainloop()