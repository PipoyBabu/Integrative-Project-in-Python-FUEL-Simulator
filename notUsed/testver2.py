from datetime import datetime, timedelta
import requests
import tkinter as tk
from tkinter import ttk
from enum import Enum
import pandas as pd
from urllib.request import urlopen
import json
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# =========================
# CONSTANTS
# =========================
LITERS_PER_BARREL = 158.98
VAT_RATE = 0.12
# =========================
# MARKET DATA ENGINE
# =========================
def fetch_exchange_rate():
    try:
        url = 'https://www.floatrates.com/daily/usd.json'
        response = urlopen(url)
        data = json.loads(response.read())
        return data['php']['rate']
    except:
        return 56.0  # fallback
def fetch_latest_brent_price():
    df = pd.read_csv("crude_oil_brent.csv", parse_dates=["Date"])
    latest_row = df.loc[df["Date"].idxmax()]
    return float(latest_row["Price"])
class FuelPriceEngine:
    def __init__(self, crude_price_usd, exchange_rate_php):
        self.base_php_per_liter = (
            crude_price_usd / LITERS_PER_BARREL
        ) * exchange_rate_php
        self.refining_freight = 15.0
        self.industry_margin = 9.0
        self.gas_excise_tax = 10.0
        self.diesel_excise_tax = 6.0
        self.premium_additive = 2.0
        self.diesel_additive = 1.5
    def _apply_vat(self, subtotal):
        return subtotal * (1 + VAT_RATE)
    def unleaded(self):
        subtotal = (
            self.base_php_per_liter
            + self.refining_freight
            + self.industry_margin
            + self.gas_excise_tax
        )
        return self._apply_vat(subtotal)
    def premium(self):
        subtotal = (
            self.base_php_per_liter
            + self.refining_freight
            + self.industry_margin
            + self.gas_excise_tax
            + self.premium_additive
        )
        return self._apply_vat(subtotal)
    def diesel(self):
        diesel_margin = self.industry_margin + 25
        subtotal = (
            self.base_php_per_liter
            + self.refining_freight
            + diesel_margin
            + self.diesel_excise_tax
        )
        return self._apply_vat(subtotal)
    def premium_diesel(self):
        diesel_margin = self.industry_margin + 30
        subtotal = (
            self.base_php_per_liter
            + self.refining_freight
            + diesel_margin
            + self.diesel_excise_tax
            + self.diesel_additive
        )
        return self._apply_vat(subtotal)
# =========================
# PUMP STATE MACHINE
# =========================
class PumpState(Enum):
    IDLE = 1
    DISPENSING = 2
    COMPLETED = 3
class PumpController:
    FLOW_RATE = 0.05  # liters per tick
    def __init__(self, price):
        self.price_per_liter = price
        self.state = PumpState.IDLE
        self.liters = 0
        self.total_cost = 0
        self.target_amount = None
    def start(self, target_amount):
        self.state = PumpState.DISPENSING
        self.target_amount = target_amount
    def update(self):
        if self.state != PumpState.DISPENSING:
            return
        self.liters += self.FLOW_RATE
        self.total_cost = self.liters * self.price_per_liter
        if self.total_cost >= self.target_amount:
            self.stop()
    def stop(self):
        self.state = PumpState.COMPLETED
    def reset(self):
        self.state = PumpState.IDLE
        self.liters = 0
        self.total_cost = 0
        self.target_amount = None
def fetch_exchange_history():
    # Mock data since the API requires an access key
    from datetime import datetime, timedelta
    dates = []
    rates = []
    base_rate = 56.0  # current rate
    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        # Simulate some variation
        rate = base_rate + (i - 15) * 0.1  # slight variation
        dates.append(date)
        rates.append(rate)
    return dates, rates
# =========================
# GUI
# =========================
class PumpGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Philippine Fuel Pump Simulator")
        self.load_market_prices()
        self.create_widgets()
    def load_market_prices(self):
        exchange_rate = fetch_exchange_rate()
        crude_price = fetch_latest_brent_price()
        engine = FuelPriceEngine(crude_price, exchange_rate)
        self.prices = {
            "Unleaded": engine.unleaded(),
            "Premium": engine.premium(),
            "Diesel": engine.diesel(),
            "Premium Diesel": engine.premium_diesel()
        }
    def create_widgets(self):
        # Root layout: top controls, bottom plot
        self.control_frame = ttk.Frame(self.root, padding=8)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(self.control_frame, text="Select Fuel:", font=(None, 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 4))
        self.selected_fuel = tk.StringVar(value="Unleaded")

        for i, fuel in enumerate(self.prices, start=1):
            ttk.Radiobutton(
                self.control_frame,
                text=f"{fuel} (₱{self.prices[fuel]:.2f}/L)",
                variable=self.selected_fuel,
                value=fuel
            ).grid(row=i, column=0, sticky="w", padx=2, pady=1)

        ttk.Label(self.control_frame, text="Enter Amount (PHP):").grid(row=0, column=1, sticky="w", padx=(24, 4))
        self.amount_entry = ttk.Entry(self.control_frame)
        self.amount_entry.grid(row=1, column=1, sticky="we", padx=(24, 4))
        self.amount_entry.insert(0, "100")

        ttk.Button(self.control_frame, text="Start Pump", command=self.start_pump).grid(row=2, column=1, sticky="we", padx=(24, 4), pady=(8, 2))
        ttk.Button(self.control_frame, text="Reset", command=self.reset).grid(row=3, column=1, sticky="we", padx=(24, 4), pady=2)

        self.display = ttk.Label(self.control_frame, text="Pump Ready", font=("Courier", 10), anchor="w", justify="left")
        self.display.grid(row=4, column=0, columnspan=2, sticky="we", pady=(8,0))

        self.history_button = ttk.Button(self.control_frame, text="Show Exchange Rate History", command=self.show_exchange_graph)
        self.history_button.grid(row=5, column=0, columnspan=2, sticky="we", pady=(8, 0))

        self.control_frame.columnconfigure(1, weight=1)

        # Plot area
        self.plot_frame = ttk.Frame(self.root, padding=8)
        self.plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.fig = None
        self.canvas = None
    def start_pump(self):
        fuel = self.selected_fuel.get()
        if not fuel:
            return
        payment = float(self.amount_entry.get())
        price = self.prices[fuel]
        self.controller = PumpController(price)
        self.controller.start(payment)
        self.run_simulation()
    def run_simulation(self):
        if self.controller.state == PumpState.DISPENSING:
            self.controller.update()
            self.update_display()
            self.root.after(100, self.run_simulation)
        else:
            self.update_display()
    def update_display(self):
        self.display.config(
            text=(
                f"Liters: {self.controller.liters:.2f} L\n"
                f"Total: ₱{self.controller.total_cost:.2f}\n"
                f"State: {self.controller.state.name}"
            )
        )
    def reset(self):
        self.controller.reset()
        self.display.config(text="Pump Ready")
    def show_exchange_graph(self):
        dates, rates = fetch_exchange_history()
        if self.fig is None:
            self.fig, ax = plt.subplots(figsize=(6,4))
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        else:
            self.fig.clear()
        ax = self.fig.add_subplot(111)
        ax.plot(dates, rates)
        ax.set_title("USD to PHP Exchange Rate (Last 30 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("PHP per USD")
        ax.grid(True)
        self.canvas.draw()
# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = PumpGUI(root)
    root.mainloop()
