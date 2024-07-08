import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        print("City not found. Please enter a valid city name.")
        return None, None


def convert_area_to_square_meters(area: float, unit: str) -> float:
    conversion_factors = {
        'acre': 4046.86,
        'yard': 0.836127,
        'square meter': 1.0
    }
    converted_area = area * conversion_factors[unit]
    print(f"--> Converted area: {area} {unit} = {converted_area:.2f} square meters")
    return converted_area

def calculate_solar_energy(area: float, average_dni: float) -> float:
    # assumed here but like we can also ask him about what kind of place so as per different kind of solar panel like silicon based, perkovsite, etc
    efficiency = 0.15
    energy = area * average_dni * efficiency * 24
    energy = energy / 1000
    # the above formula needs to be optimized which we will be doing next
    print(f"--> Calculated solar energy: {energy:.2f} kWh/day from {area:.2f} square meters with {average_dni/1000.0 : .2f} kWh/m²/day insolation")
    return energy

# just passed here for reference but we will train chatbot 
def estimate_daily_usage(energy_kwh: float) -> list:
    usages = [
        {"device": "LED light bulb (10W)", "usage": 0.01, "duration": "hours"},
        {"device": "Laptop", "usage": 0.05, "duration": "hours"},
        {"device": "Refrigerator", "usage": 1.5, "duration": "hours"},
        {"device": "Washing Machine", "usage": 2.0, "duration": "loads"},
        {"device": "Electric Car (per mile)", "usage": 0.3, "duration": "miles"}
    ]
    estimates = []
    for use in usages:
        estimate = energy_kwh / use["usage"]
        estimates.append(f"{estimate:.2f} {use['duration']} of {use['device']}")
        print(f"--> Estimated {use['device']}: {estimate:.2f} {use['duration']}")
    return estimates

def calculate_cost_savings(energy_kwh: float, rate_per_kwh: float) -> float:
    cost_savings = energy_kwh * rate_per_kwh
    print(f"--> Calculated cost savings: Rs {cost_savings:.2f} per day")
    return cost_savings
