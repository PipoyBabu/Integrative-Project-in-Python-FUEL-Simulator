import customtkinter as ctk
from urllib.request import urlopen
import json
import pandas as pd
from PIL import Image

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
        self.current_page = "Fuel Pump"

        self.colors = self.get_colors()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, fg_color=self.colors["sidebar_bg"])
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main = ctk.CTkFrame(self, fg_color=self.colors["main_bg"])
        self.main.grid(row=0, column=1, sticky="nsew")

        ctk.CTkButton(
            self.main,
            text="☰",
            width=40,
            fg_color="transparent",
            command=self.toggle_sidebar
        ).pack(anchor="nw", padx=12, pady=12)

        self.content = ctk.CTkFrame(self.main, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=10, pady=10)

        self.build_sidebar()
        self.show_page("Fuel Pump")

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def relative_luminance(self, rgb):
        def channel(c):
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * channel(rgb[0]) + 0.7152 * channel(rgb[1]) + 0.0722 * channel(rgb[2])

    def get_contrast_text_color(self, bg_color):
        rgb = self.hex_to_rgb(bg_color)
        lum = self.relative_luminance(rgb)
        return "#000000" if lum > 0.50 else "#FFFFFF"

    def get_colors(self):
        mode = ctk.get_appearance_mode()
        if mode == "Dark":
            main_bg = "#1a1a1a"
            sidebar_bg = "#2b2b2b"
            content_bg = "#333333"
            sidebar_text = "#FFFFFF"
            content_text = "#FFFFFF"
        else:
            main_bg = "#f3f4f6"
            sidebar_bg = "#13389D"
            content_bg = "#e5e7eb"
            sidebar_text = "#FFFFFF"
            content_text = "#000000"

        return {
            "sidebar_bg": sidebar_bg,
            "main_bg": main_bg,
            "sidebar_text": sidebar_text,
            "content_text": content_text,
            "content_bg": content_bg
        }

    def build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Seekseven", text_color=self.colors["sidebar_text"]).pack(pady=15)

        for item in ["Dashboard", "Delivery Schedule", "Fuel Pump", "Settings"]:
            ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                text_color=self.colors["sidebar_text"],
                command=lambda b=item: self.change_page(b)
            ).pack(fill="x", padx=20, pady=5)

        self.side_toggle = ctk.CTkButton(
            self.sidebar,
            text="❮",
            width=20,
            height=40,
            fg_color="transparent",
            text_color=self.colors["sidebar_text"],
            command=self.toggle_sidebar
        )
        self.side_toggle.place(relx=1.0, rely=0.5, anchor="e", x=-6)

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
        self.current_page = name
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
        frame = ctk.CTkFrame(self.content, fg_color=self.colors["main_bg"])

        ctk.CTkLabel(frame, text="Dashboard", font=("Arial", 24, "bold"), text_color=self.colors["content_text"]).pack(pady=10)

        # ✅ ADDED OIL PRICES
        prices = get_prices()
        price_frame = ctk.CTkFrame(frame, fg_color=self.colors["content_bg"])
        price_frame.pack(pady=10, padx=10, fill="x")

        for fuel, price in prices.items():
            ctk.CTkLabel(
                price_frame,
                text=f"{fuel}: ₱{price}/L",
                font=("Arial", 14, "bold"),
                text_color=self.colors["content_text"]
            ).pack(side="left", padx=20, pady=10)

        df = pd.DataFrame({
            "date": pd.date_range(start="2024-01-01", periods=10),
            "users": [100,120,130,90,150,170,160,180,200,210],
            "product": ["A","B","A","C","B","A","C","B","A","C"],
            "sales": [10,20,15,5,25,30,10,22,18,9]
        })

        selected_product = ctk.StringVar(value="All")

        def update_chart(choice):
            filtered = df if choice == "All" else df[df["product"] == choice]

            for widget in chart_frame.winfo_children():
                widget.destroy()

            # ✅ FIXED LINE CHART
            fig1, ax1 = plt.subplots(figsize=(5,4))
            ax1.plot(filtered["date"], filtered["users"], marker='o')
            ax1.set_title("Daily Active Users")
            ax1.set_xlabel("Date")
            ax1.set_ylabel("Users")
            ax1.tick_params(axis='x', rotation=45)
            fig1.tight_layout()

            canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame)
            canvas1.draw()
            canvas1.get_tk_widget().pack(side="left", fill="both", expand=True)

            grouped = filtered.groupby("product")["sales"].sum()

            # ✅ FIXED BAR CHART
            fig2, ax2 = plt.subplots(figsize=(5,4))
            ax2.bar(grouped.index, grouped.values)
            ax2.set_title("Top Selling Products")
            ax2.set_xlabel("Product")
            ax2.set_ylabel("Sales")
            fig2.tight_layout()

            canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame)
            canvas2.draw()
            canvas2.get_tk_widget().pack(side="left", fill="both", expand=True)

        dropdown = ctk.CTkOptionMenu(
            frame,
            values=["All"] + list(df["product"].unique()),
            variable=selected_product,
            command=update_chart
        )
        dropdown.pack(pady=10)

        chart_frame = ctk.CTkFrame(frame)
        chart_frame.pack(fill="both", expand=True)

        update_chart("All")

        return frame

    # DELIVERY SCHEDULE (UNCHANGED)
    def create_delivery_page(self):
        frame = ctk.CTkFrame(self.content, fg_color=self.colors["main_bg"])

        ctk.CTkLabel(frame, text="Delivery Schedule", font=("Arial", 24, "bold"), text_color=self.colors["content_text"]).pack(pady=20)

        date_entry = ctk.CTkEntry(frame, placeholder_text="Enter date (YYYY-MM-DD)", text_color=self.colors["content_text"])
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

    # SETTINGS (UNCHANGED)
    def create_settings_page(self):
        frame = ctk.CTkFrame(self.content, fg_color=self.colors["main_bg"])

        ctk.CTkLabel(frame, text="Settings", font=("Arial", 24, "bold"), text_color=self.colors["content_text"]).pack(pady=20)
        ctk.CTkLabel(frame, text="Appearance Mode", text_color=self.colors["content_text"]).pack(pady=10)

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
        self.colors = self.get_colors()
        self.sidebar.configure(fg_color=self.colors["sidebar_bg"])
        self.main.configure(fg_color=self.colors["main_bg"])
        # Update sidebar labels and buttons
        for widget in self.sidebar.winfo_children():
            if isinstance(widget, ctk.CTkLabel) or isinstance(widget, ctk.CTkButton):
                widget.configure(text_color=self.colors["sidebar_text"])
        # Refresh the current page to update colors
        self.show_page(self.current_page)

    # FUEL PAGE (UNCHANGED)
    def create_fuel_page(self):
        frame = ctk.CTkFrame(self.content, fg_color=self.colors["main_bg"])
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        frame.grid_columnconfigure(0, weight=2)
        frame.grid_columnconfigure(1, weight=1)

        data = get_prices()

        left = ctk.CTkFrame(frame, fg_color=self.colors["content_bg"])
        left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(left, text="Vehicle Preview", font=("Arial", 16, "bold"), text_color=self.colors["content_text"]).pack(pady=10)

        vehicle_display = ctk.CTkLabel(left, text="Sedan", font=("Arial", 18, "bold"), text_color=self.colors["content_text"])
        vehicle_display.pack(pady=10)

        preview = ctk.CTkFrame(left, height=200, fg_color=self.colors["main_bg"])
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

        right = ctk.CTkFrame(frame, fg_color=self.colors["content_bg"])
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        trivia_frame = ctk.CTkFrame(frame, fg_color=self.colors["content_bg"])
        trivia_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=(10, 0))

        self.trivia_label = ctk.CTkLabel(
            trivia_frame,
            text="",
            wraplength=900,
            justify="left",
            text_color=self.colors["content_text"],
            font=("Arial", 12)
        )
        self.trivia_label.pack(fill="x", pady=10, padx=10)

        self.max_liters_label = ctk.CTkLabel(
            trivia_frame,
            text="",
            text_color=self.colors["content_text"],
            font=("Arial", 12, "bold")
        )
        self.max_liters_label.pack(fill="x", pady=(0, 5), padx=10)

        self.remaining_label = ctk.CTkLabel(
            trivia_frame,
            text="",
            text_color=self.colors["content_text"],
            font=("Arial", 12)
        )
        self.remaining_label.pack(fill="x", pady=(0, 10), padx=10)

        vehicle_buttons = {}

        trivia_by_vehicle = {
            "Motorcycle": "Motorcycles usually have smaller tanks (12-18L), good for city riding and quick fill-ups.",
            "Sedan": "Sedans average 45-55L; they balance fuel capacity and efficiency for daily commutes.",
            "SUV": "SUVs often hold 60-75L since they carry more passengers and cargo on longer drives.",
            "Truck": "Pickup trucks can be 100-150L; heavy loads and towing require larger tanks.",
        }

        max_liters_by_vehicle = {
            "Motorcycle": 16.0,
            "Sedan": 50.0,
            "SUV": 70.0,
            "Truck": 130.0,
        }

        state = {"running": False, "liters": 0, "price": 0, "target": 0, "max_liters": 0}

        def select_vehicle(name):
            if state["running"]:
                return
            vehicle_display.configure(text=name)
            preview_label.configure(image=self.vehicle_images[name])
            self.trivia_label.configure(text=f"Trivia: {trivia_by_vehicle[name]}")
            self.max_liters = max_liters_by_vehicle[name]
            self.max_liters_label.configure(text=f"Max capacity: {self.max_liters:.1f} L")
            self.remaining_label.configure(text=f"Max liters remaining: {self.max_liters:.1f} L")
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
            btn.pack(side="left", padx=8, pady=6)
            vehicle_buttons[v] = btn

        select_vehicle("Sedan")

        selected = ctk.StringVar(value="Unleaded")

        ctk.CTkLabel(right, text="Fuel Type", text_color=self.colors["content_text"]).pack(pady=5)

        for fuel, price in data.items():
            ctk.CTkRadioButton(
                right,
                text=f"{fuel} ₱{price}/L",
                variable=selected,
                value=fuel,
                text_color=self.colors["content_text"]
            ).pack(anchor="w", padx=10)

        entry = ctk.CTkEntry(right, placeholder_text="Enter amount (₱)", text_color=self.colors["content_text"])
        entry.pack(pady=10)

        display = ctk.CTkLabel(right, text="0.00 L\n₱0.00", font=("Arial", 18, "bold"), text_color=self.colors["content_text"])
        display.pack(pady=15)

        state = {"running": False, "liters": 0, "price": 0, "target": 0, "max_liters": 0}

        self.start_btn = ctk.CTkButton(right, text="Start Pump", text_color=self.colors["content_text"])
        self.start_btn.pack(pady=5)

        self.stop_btn = ctk.CTkButton(right, text="Stop", text_color=self.colors["content_text"])
        self.stop_btn.pack(pady=5)

        self.reset_btn = ctk.CTkButton(right, text="Reset", text_color=self.colors["content_text"])
        self.reset_btn.pack(pady=5)

        def start():
            try:
                state["price"] = data[selected.get()]
                money_target = float(entry.get())
                state["liters"] = 0
                state["running"] = True
                state["max_liters"] = getattr(self, "max_liters", 0)

                if state["max_liters"] <= 0:
                    display.configure(text="Select a vehicle first")
                    state["running"] = False
                    return

                max_money = state["max_liters"] * state["price"]
                if money_target > max_money:
                    state["target"] = max_money
                else:
                    state["target"] = money_target

                self.start_btn.configure(fg_color="green")
                self.stop_btn.configure(fg_color="#3b82f6")
                self.reset_btn.configure(fg_color="#3b82f6")
                for btn in vehicle_buttons.values():
                    btn.configure(state="disabled")

                pump_loop()
            except ValueError:
                display.configure(text="Invalid input")

        def stop():
            state["running"] = False
            self.stop_btn.configure(fg_color="red")
            self.start_btn.configure(fg_color="#3b82f6")
            self.reset_btn.configure(fg_color="#3b82f6")
            for btn in vehicle_buttons.values():
                btn.configure(state="normal")

        def reset():
            state["running"] = False
            state["liters"] = 0
            display.configure(text="0.00 L\n₱0.00")
            self.remaining_label.configure(text=f"Max liters remaining: {state['max_liters']:.1f} L")

            self.reset_btn.configure(fg_color="orange")
            self.start_btn.configure(fg_color="#3b82f6")
            self.stop_btn.configure(fg_color="#3b82f6")
            for btn in vehicle_buttons.values():
                btn.configure(state="normal")

        self.start_btn.configure(command=start)
        self.stop_btn.configure(command=stop)
        self.reset_btn.configure(command=reset)

        def pump_loop():
            if not state["running"]:
                return

            state["liters"] += 0.05
            if state["liters"] >= state["max_liters"]:
                state["liters"] = state["max_liters"]
                state["running"] = False

            total = state["liters"] * state["price"]

            if total >= state["target"]:
                total = state["target"]
                state["liters"] = total / state["price"]
                state["running"] = False

            if state["liters"] >= state["max_liters"]:
                state["running"] = False

            remaining = max(0, state["max_liters"] - state["liters"])
            self.remaining_label.configure(text=f"Max liters remaining: {remaining:.2f} L")

            display.configure(text=f"{state['liters']:.2f} L\n₱{total:.2f}")

            if not state["running"]:
                if state['liters'] >= state['max_liters']:
                    display.configure(text=f"{state['liters']:.2f} L\n₱{total:.2f}")
                    self.remaining_label.configure(text="Max capacity reached")
                for btn in vehicle_buttons.values():
                    btn.configure(state="normal")
                return

            frame.after(80, pump_loop)

        return frame


if __name__ == "__main__":
    app = App()
    app.mainloop()