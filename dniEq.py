import requests
import numpy as np
import pandas as pd
import os
from geopy.geocoders import Nominatim
import datetime
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    else:
        print("City not found. Please enter a valid city name.")
        return None, None
    
def fetch_city_dni_eqn_today(latitude, longitude, city_name):
    os.makedirs('24hr_Data/DNI', exist_ok=True)
    # latitude, longitude = get_coordinates(city_name)

    base_url = r"https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=ALLSKY_SFC_SW_DNI&community=RE&longitude={longitude}&latitude={latitude}&start=20221231&end=20240101&format=JSON"

    if latitude:
        s_dni = []
        cd = np.array([0] * 8808)
        # for i , j in df.iterrows() :
        #     print(i)
        api_url = base_url.format(latitude=latitude,longitude=longitude)
        res = requests.get(url = api_url , verify = True , timeout = 40.00)
        jsn = res.json()
        data = jsn['properties']['parameter']
        df1 = pd.DataFrame(data)
        curr_dni = np.array(df1['ALLSKY_SFC_SW_DNI'])
        cd = np.add(cd , curr_dni)
                    
        # cd = np.true_divide(cd)
        cd = cd[19 : 8803]
        i = 0
        year_cd = []
        while i < 8784 :
            day_cd = []
            j = i
            while i < min(j + 24 , 8784) :
                day_cd.append(cd[i])
                i += 1
            year_cd.append(day_cd)
            
        dni = pd.DataFrame(year_cd)
        # Ensure the directory is writable
        output_dir = '24hr_Data/DNI/'
        output_path = os.path.join(output_dir, f'{city_name}.csv')

        dni.to_csv(output_path, index=False)

        # Check if the file was created successfully
        if os.path.exists(output_path):
            print(f"CSV file created successfully: {output_path}")
        else:
            print("Failed to create CSV file.")
                    
    else:
        print("Wrong Input")
        
    # get solar insolation

    # Read the KANPUR.csv file
    city_df = pd.read_csv(f'24hr_Data/DNI/{city_name}.csv')

    # Get today's date
    today = datetime.date.today()

    # Calculate the day number
    start_date=datetime.date(2022, 12, 31)
    today = today.replace(year=start_date.year)
    if today < start_date:
        # If date is before the start_date, consider it as next year
        today = today.replace(year=start_date.year + 1)
    day_number = (today - start_date).days + 1
    
    print(f"Day number for {today} is {day_number-1}")

    # Check if the day_number is within the range of the DataFrame
    if day_number > len(city_df):
        raise ValueError("The day number exceeds the length of the data in KANPUR.csv")

    # Get the row for the calculated day number
    day_data = city_df.iloc[day_number - 1]  # Subtract 1 because DataFrame is 0-indexed

    # Convert the row data to a numpy array
    day_data_array = day_data.to_numpy()
    hours = np.arange(24)
    
    # Polynomial fitting (degree 3 for example)
    coefficients = np.polyfit(hours, day_data_array, deg=4)
    poly_func = np.poly1d(coefficients)
    poly_eqn = " + ".join([f"{coeff:.2f}*x^{i}" if i > 0 else f"{coeff:.5f}" for i, coeff in enumerate(coefficients[::-1])])
    # Spline interpolation
    spline_func = CubicSpline(hours, day_data_array)

    # Plot the data and the fits
    plt.figure(figsize=(10, 6))
    plt.plot(hours, day_data_array, 'o', label='Hourly Data')
    plt.plot(hours, poly_func(hours), '-', label='Polynomial Fit')
    plt.plot(hours, spline_func(hours), '--', label='Spline Interpolation')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Data')
    plt.legend()
    plt.title('Hourly Data Fitting')
    plt.grid(True)
    
    plt.show()

    # print(f"Polynomial fit value at time {time}: {poly_value}")
    # print(f"Spline interpolation value at time {time}: {spline_value}")
    print(f'the dni equation for {today} is: ({poly_eqn})')
    return poly_eqn

city_name = input("Enter your city: ")    
latitude, longitude = get_coordinates(city_name)
dni_eqn = fetch_city_dni_eqn_today(latitude,longitude,city_name)

