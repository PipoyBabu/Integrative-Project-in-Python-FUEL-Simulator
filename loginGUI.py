# type: ignore
import customtkinter as ctk
from urllib.request import urlopen
import json
import pandas as pd
from datetime import datetime, timedelta


ctk.set_appearance_mode("light")
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
        return None




class App(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.geometry("1000x650")
        self.title("Seekseven")


        self.sidebar_visible = True


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
            hover_color="#1e3a8a",
            text_color="white",
            corner_radius=0,
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


    def create_fuel_page(self):
        frame = ctk.CTkFrame(self.content)
        frame.pack(fill="both", expand=True, padx=20, pady=20)


        frame.grid_columnconfigure(0, weight=2)
        frame.grid_columnconfigure(1, weight=1)


        data = get_prices()


        # ================= LEFT PANEL =================
        left = ctk.CTkFrame(frame, fg_color="#e5e7eb")
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)


        ctk.CTkLabel(left, text="Vehicle Preview", font=("Arial", 16, "bold")).pack(pady=10)


        vehicle_var = ctk.StringVar(value="Sedan")


        vehicle_display = ctk.CTkLabel(
            left,
            text="Sedan",
            font=("Arial", 18, "bold")
        )
        vehicle_display.pack(pady=10)


        preview = ctk.CTkFrame(left, height=200, fg_color="white")
        preview.pack(fill="x", padx=20, pady=10)


        preview_label = ctk.CTkLabel(preview, text="NO IMAGE")
        preview_label.pack(expand=True)


        vehicle_frame = ctk.CTkFrame(left, fg_color="transparent")
        vehicle_frame.pack(pady=10)


        vehicle_buttons = {}


        def select_vehicle(name):
            vehicle_var.set(name)
            vehicle_display.configure(text=name)
            preview_label.configure(text=name)


            for v, btn in vehicle_buttons.items():
                if v == name:
                    btn.configure(fg_color="#2563eb")
                else:
                    btn.configure(fg_color="gray")


        vehicles = ["Motorcycle", "Sedan", "SUV", "Truck"]


        for v in vehicles:
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


        # ================= RIGHT PANEL =================
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


        display = ctk.CTkLabel(
            right,
            text="0.00 L\n₱0.00",
            font=("Arial", 18, "bold")
        )
        display.pack(pady=15)


        state = {"running": False, "liters": 0, "price": 0, "target": 0}


        def start():
            try:
                state["price"] = data[selected.get()]
                state["target"] = float(entry.get())
                state["liters"] = 0
                state["running"] = True
                pump_loop()
            except:
                display.configure(text="Invalid input")


        def pump_loop():
            if not state["running"]:
                return


            state["liters"] += 0.05
            total = state["liters"] * state["price"]


            if total >= state["target"]:
                total = state["target"]
                state["liters"] = total / state["price"]
                state["running"] = False


            display.configure(
                text=f"{state['liters']:.2f} L\n₱{total:.2f}"
            )


            if state["running"]:
                frame.after(80, pump_loop)


        def stop():
            state["running"] = False


        def reset():
            state["running"] = False
            state["liters"] = 0
            display.configure(text="0.00 L\n₱0.00")


        ctk.CTkButton(right, text="Start Pump", command=start).pack(pady=5)
        ctk.CTkButton(right, text="Stop", command=stop).pack(pady=5)
        ctk.CTkButton(right, text="Reset", command=reset).pack(pady=5)


        return frame




if __name__ == "__main__":
    app = App()
    app.mainloop()

