# Real-time Solar Energy Estimation Tool

## Overview
The Solar Energy Estimation Tool is a Python-based application designed to calculate potential solar energy generation and cost savings based on geographical location and user-provided inputs. It utilizes NASA's POWER API to fetch real-time Direct Normal Irradiance (DNI) data, which is crucial for estimating solar insolation.

## Features
- **Real-Time Data Retrieval**: Fetches hourly solar irradiance data from NASA's POWER API based on user-specified geographical coordinates.
- **Solar Energy Calculation**: Computes daily solar energy generation potential using algorithms that integrate DNI data with user-provided area details.
- **Cost Savings Estimation**: Estimates potential cost savings on electricity bills by switching to solar energy based on user-provided electricity rates.
- **Interactive GUI**: Provides a user-friendly PyQt5-based interface for users to input their location, area, and electricity rate, visualizing results in real-time.

## Features coming in future
- **Optimization**: Using gurobipy, I will optimize the program to get minimum number of solar panels required to satisfy consumers usage.
- **EV & LPG tool**: Similar tool for electric vehicles and LPG where users budget will be minimized according to inputs.

## Technologies Used
- Python
- Libraries:
  - numpy
  - geopy
  - PyQt5
  - datetime
  - requests
- NASA's POWER API

## Usage
1. Clone the repository:
```bash
git clone https://github.com/your/repository.git
```
2. Install dependencies:
```bash
pip install -r numpy requests geopy PyQt5
```
3. Run the application:
```bash
python main.py
```
4. Enter your city, rooftop area, and electricity rate to calculate solar energy potential and cost savings.


made by: [Aryan Nigam](https://github.com/aru20112233)
