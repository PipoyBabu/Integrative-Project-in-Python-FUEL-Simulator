import customtkinter as ctk
from urllib.request import urlopen
import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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


def get_exchange_history():
    dates = []
    rates = []
    base = 56

    for i in range(30):
        date = datetime.now() - timedelta(days=29 - i)
        rate = base + (i - 15) * 0.1
        dates.append(date)
        rates.append(rate)

    return dates, rates


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("390x844")
        self.title("Seekseven")
        self.configure(fg_color="#f3f4f6")

        self.sidebar_width = 260
        self.sidebar_visible = False

        self.topbar = ctk.CTkFrame(self, height=60, fg_color="white")
        self.topbar.pack(fill="x")

        ctk.CTkButton(self.topbar, text="☰", width=40,
                      fg_color="transparent",
                      command=self.toggle_sidebar).pack(side="left", padx=10)

        self.title_label = ctk.CTkLabel(self.topbar, text="Fleet Dashboard",
                                       font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=10)

        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.pack(fill="both", expand=True, padx=10, pady=10)

        self.sidebar = ctk.CTkFrame(self, width=260, fg_color="#13389D")
        self.sidebar.place(x=-260, y=0, relheight=1)

        self.build_sidebar()
        self.show_page("Dashboard")

    def build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Seekseven",
                     text_color="white").pack(pady=20)

        for item in ["Dashboard", "Delivery Schedule", "Fuel Pump", "Settings"]:
            ctk.CTkButton(
                self.sidebar,
                text=item,
                fg_color="transparent",
                text_color="white",
                command=lambda b=item: self.change_page(b)
            ).pack(fill="x", padx=20, pady=5)

    def change_page(self, name):
        self.show_page(name)
        self.slide_out()

    def show_page(self, name):
        for w in self.content.winfo_children():
            w.destroy()

        if name == "Dashboard":
            self.create_home_page().pack(fill="both", expand=True)
        elif name == "Delivery Schedule":
            self.create_fleet_page().pack(fill="both", expand=True)
        elif name == "Fuel Pump":
            self.create_fuel_page().pack(fill="both", expand=True)
        elif name == "Settings":
            self.create_settings_page().pack(fill="both", expand=True)

        self.title_label.configure(text=name)

    def create_home_page(self):
        frame = ctk.CTkScrollableFrame(self.content)
        frame.grid_columnconfigure((0, 1), weight=1)

        data = get_prices()

        if data:
            cards = [
                ("Unleaded", f"₱{data['Unleaded']}"),
                ("Premium", f"₱{data['Premium']}"),
                ("Diesel", f"₱{data['Diesel']}")
            ]
        else:
            cards = [("Error", "No Data")]

        for i, (title, value) in enumerate(cards):
            card = ctk.CTkFrame(frame, height=120)
            card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="nsew")

            ctk.CTkLabel(card, text=title).pack(anchor="w", padx=10)
            ctk.CTkLabel(card, text=value,
                         font=("Arial", 20, "bold")).pack(anchor="w", padx=10)

        graph_frame = ctk.CTkFrame(frame)
        graph_frame.grid(row=5, column=0, columnspan=2, padx=8, pady=10, sticky="nsew")

        holder = {"canvas": None}

        def toggle_graph():
            if holder["canvas"]:
                holder["canvas"].get_tk_widget().destroy()
                holder["canvas"] = None
                return

            dates, rates = get_exchange_history()

            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.plot(dates, rates, marker='o', color='#1f77b4', linewidth=2, markersize=5)
            ax.set_title("USD → PHP (30 days)", fontsize=14, fontweight='bold')
            ax.set_xlabel("Date", fontsize=11)
            ax.set_ylabel("Exchange rate", fontsize=11)
            ax.grid(True, linestyle='--', alpha=0.5)

            # improve date formatting
            ax.xaxis.set_major_locator(plt.MaxNLocator(6))
            ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%m-%d'))
            fig.autofmt_xdate(rotation=45, ha='right')

            fig.tight_layout(pad=1.2)

            canvas = FigureCanvasTkAgg(fig, master=graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            holder["canvas"] = canvas

        ctk.CTkButton(frame, text="📈", width=40,
                      command=toggle_graph).place(relx=0.95, rely=0.02)

        return frame

    def create_fleet_page(self):
        frame = ctk.CTkScrollableFrame(self.content)
        ctk.CTkLabel(frame, text="No delivery schedule yet").pack(pady=50)
        return frame

    def create_fuel_page(self):
        frame = ctk.CTkFrame(self.content)

        data = get_prices()

        if not data:
            ctk.CTkLabel(frame, text="No data").pack(pady=50)
            return frame

        selected = ctk.StringVar(value="Unleaded")

        for fuel, price in data.items():
            ctk.CTkRadioButton(
                frame,
                text=f"{fuel} ₱{price}/L",
                variable=selected,
                value=fuel
            ).pack(anchor="w", padx=20)

        entry = ctk.CTkEntry(frame, placeholder_text="Enter amount (₱)")
        entry.pack(pady=10)

        display = ctk.CTkLabel(frame, text="0.00 L\n₱0.00",
                               font=("Arial", 18, "bold"))
        display.pack(pady=15)

        state = {"run": False, "liters": 0, "price": 0, "target": 0}

        def start():
            try:
                state["price"] = data[selected.get()]
                state["target"] = float(entry.get())
                state["liters"] = 0
                state["run"] = True
                loop()
            except:
                display.configure(text="Invalid input")

        def loop():
            if not state["run"]:
                return

            state["liters"] += 0.05
            total = state["liters"] * state["price"]

            if total >= state["target"]:
                total = state["target"]
                state["liters"] = total / state["price"]
                state["run"] = False

            display.configure(text=f"{state['liters']:.2f} L\n₱{total:.2f}")

            if state["run"]:
                frame.after(100, loop)

        def stop():
            state["run"] = False

        def reset():
            state["run"] = False
            state["liters"] = 0
            display.configure(text="0.00 L\n₱0.00")

        ctk.CTkButton(frame, text="Start Pump", command=start).pack(pady=5)
        ctk.CTkButton(frame, text="Stop", command=stop).pack(pady=5)
        ctk.CTkButton(frame, text="Reset", command=reset).pack(pady=5)

        return frame

    def create_settings_page(self):
        frame = ctk.CTkScrollableFrame(self.content)

        switch = ctk.CTkSwitch(
            frame,
            text="Dark Mode",
            command=lambda: ctk.set_appearance_mode(
                "dark" if switch.get() else "light"
            )
        )
        switch.pack(pady=20)

        return frame

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.place(x=-260)
        else:
            self.sidebar.place(x=0)

        self.sidebar_visible = not self.sidebar_visible


if __name__ == "__main__":
    app = App()
    app.mainloop()