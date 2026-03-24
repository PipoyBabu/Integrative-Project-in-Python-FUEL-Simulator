# Fuel Simulator Demo (3-Minute Script)

## Overview
This is a quick 3-minute demonstration of the Fuel Simulator application, a Python-based GUI tool for simulating fuel prices and vehicle fuel calculations.

## Prerequisites
- Python 3.x installed
- Required packages: customtkinter, pandas, matplotlib, pillow, urllib

## Demo Script

### Minute 1: Launch and Dashboard (0:00 - 1:00)

1. **Launch the Application** (0:00 - 0:10)
   - Open terminal/command prompt
   - Navigate to project directory: `cd path/to/Integrative-Project-in-Python-FUEL-Simulator`
   - Run: `python mytk.py`
   - App opens in light mode, dashboard view by default

2. **Explore Dashboard** (0:10 - 0:45)
   - View current fuel prices displayed at top (Unleaded, Premium, Diesel in PHP/L)
   - Observe the two charts below:
     - Top chart: Crude Oil Brent Prices Over Time (line chart showing historical prices)
     - Bottom chart: Current Fuel Prices (bar chart comparing fuel types)
   - Charts use real data from crude_oil_brent.csv and calculated prices

3. **Sidebar Navigation** (0:45 - 1:00)
   - Click hamburger menu (☰) to toggle sidebar
   - Note navigation options: Dashboard, Delivery Schedule, Fuel Pump, Settings

### Minute 2: Fuel Pump Simulation (1:00 - 2:00)

1. **Switch to Fuel Pump** (1:00 - 1:05)
   - Click "Fuel Pump" in sidebar
   - Page loads with vehicle selection and fuel calculation

2. **Vehicle Selection** (1:05 - 1:30)
   - Left panel shows vehicle preview
   - Click vehicle buttons: Motorcycle, Sedan, SUV, Truck
   - Watch image change and tank capacity update
   - Note trivia text changes for each vehicle type

3. **Fuel Calculation** (1:30 - 1:50)
   - Right panel shows fuel prices and calculator
   - Select fuel type (Unleaded/Premium/Diesel)
   - Enter liters or amount
   - Calculator shows total cost and remaining tank capacity

4. **Interactive Elements** (1:50 - 2:00)
   - Try different combinations
   - Observe real-time updates

### Minute 3: Additional Features (2:00 - 3:00)

1. **Delivery Schedule** (2:00 - 2:20)
   - Click "Delivery Schedule" in sidebar
   - Add delivery dates (YYYY-MM-DD format)
   - Add/remove schedules
   - View list of scheduled deliveries

2. **Settings** (2:20 - 2:40)
   - Click "Settings" in sidebar
   - Toggle between Light/Dark mode
   - Observe theme changes across the app

3. **Data Integration** (2:40 - 3:00)
   - App fetches live USD/PHP exchange rates
   - Uses historical crude oil data
   - Calculates fuel prices based on current market data
   - Demonstrates real-world data integration

## Key Features Demonstrated
- Real-time fuel price calculations
- Historical oil price visualization
- Vehicle-specific fuel simulations
- Multi-page GUI navigation
- Theme switching
- Data persistence (CSV integration)

## Technical Highlights
- Built with CustomTkinter for modern UI
- Matplotlib integration for data visualization
- Pandas for data manipulation
- API integration for exchange rates
- Responsive design with sidebar navigation

## Conclusion
This fuel simulator demonstrates practical application of Python for data visualization, GUI development, and real-world calculations. The app successfully integrates multiple data sources and provides an intuitive interface for fuel-related simulations.

*Demo time: ~3 minutes*