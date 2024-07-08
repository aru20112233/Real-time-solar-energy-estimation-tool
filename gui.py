import requests
import numpy as np
import pandas as pd
import os
from geopy.geocoders import Nominatim
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from main import get_coordinates, convert_area_to_square_meters, calculate_solar_energy, estimate_daily_usage, calculate_cost_savings
import numpy as np
import datetime
from geopy.geocoders import GoogleV3
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

class App(QWidget):
    
    def change_button_color(self):
        # self.city_button.setStyleSheet("background-color: yellow")
        sender = self.sender()  # Get the object that triggered the slot (clicked button)
        sender.setStyleSheet("""
                QPushButton {
                    background-color: yellow;
                    color: black;
                    border: 2px solid black;
                    border-radius: 5px;
                }
                QPushButton:pressed {
                    background-color: orange;
                }
            """)
    
    def restart_process(self):
        # Reset all input fields and hide/show necessary widgets
        self.city_input.clear()
        self.city_input.show()

        self.unit_input.setCurrentIndex(0)  # Reset combo box to default selection
        self.unit_input.hide()

        self.area_input.clear()
        self.area_input.hide()

        self.rate_input.clear()
        self.rate_input.hide()

        self.calculate_button.hide()

        self.result_output.clear()

    def show_result_output(self):
        self.result_output.show()
    
    def __init__(self):
        
        super().__init__()


        self.setWindowTitle("Real-time Solar Energy Estimation")
        self.setGeometry(100, 100, 1300, 800)  # Adjusted size for better visibility

        # self.setStyleSheet("background-color: #E0FFFF;")
        self.setStyleSheet("background-color: #FFFFFF;")
        

        self.layout = QVBoxLayout()
        
         # CO2 footprint image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # Align image to center
        # Load and scale the image
        pixmap = QPixmap('image.jpg')
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)  # Align image to center
        self.layout.addWidget(self.image_label)

        # Font settings
        header_font = QFont("Arial", 12, QFont.Bold)
        label_font = QFont('Arial',14,QFont.Bold)
        font = QFont()
        font.setPointSize(12)

        # City input
        self.city_label = QLabel("Enter the city you live in:")
        self.city_label.setFont(header_font)
        self.layout.addWidget(self.city_label)

        self.city_input = QLineEdit()
        self.city_input.setFont(font)
        self.layout.addWidget(self.city_input)
        self.city_button = QPushButton("Next")
        self.city_button.setFont(font)
        self.city_button.clicked.connect(self.change_button_color)
        self.city_button.clicked.connect(self.fetch_city_data)
        self.city_button.clicked.connect(self.show_result_output)
        self.layout.addWidget(self.city_button)

        # Unit input
        self.unit_label = QLabel("Enter the unit of area (acre, yard, square meter):")
        self.unit_label.setFont(header_font)
        self.layout.addWidget(self.unit_label)
        self.unit_label.hide()

        self.unit_input = QComboBox()
        self.unit_input.setFont(font)
        self.unit_input.addItems(['acre', 'yard', 'square meter'])
        self.layout.addWidget(self.unit_input)
        self.unit_input.hide()

        # Area input
        self.area_label = QLabel("Enter the area of your roof:")
        self.area_label.setFont(header_font)
        self.layout.addWidget(self.area_label)
        self.area_label.hide()

        self.area_input = QLineEdit()
        self.area_input.setFont(font)
        self.layout.addWidget(self.area_input)
        self.area_input.hide()

        self.area_button = QPushButton("Next")
        self.area_button.setFont(font)
        self.area_button.clicked.connect(self.change_button_color)
        self.area_button.clicked.connect(self.calculate_area_and_energy)
        self.layout.addWidget(self.area_button)
        self.area_button.hide()

        # Rate input
        self.rate_label = QLabel("Enter your electricity rate in Rs/kWh:")
        self.rate_label.setFont(header_font)
        self.layout.addWidget(self.rate_label)
        self.rate_label.hide()

        self.rate_input = QLineEdit()
        self.rate_input.setFont(font)
        self.layout.addWidget(self.rate_input)
        self.rate_input.hide()

        # Calculate button
        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.setFont(font)
        self.calculate_button.clicked.connect(self.change_button_color)
        self.calculate_button.clicked.connect(self.calculate_cost_savings)
        self.layout.addWidget(self.calculate_button)
        self.calculate_button.hide()

        # Result output
        self.result_output = QTextEdit()
        self.result_output.setFont(label_font)
        self.result_output.setReadOnly(True)
        self.result_output.setStyleSheet("background-color: #FFFFFF;")
        self.layout.addWidget(self.result_output)
        self.result_output.hide()
    
        
        # Restart button
        self.restart_button = QPushButton("Restart")
        self.restart_button.clicked.connect(self.restart_process)
        self.layout.addWidget(self.restart_button)
        self.restart_button.hide()  # Initially hide the restart button

        self.setLayout(self.layout)

        # Initialize variables
        self.city_data = None
        self.solar_energy = 0
        
    def fetch_city_data(self):
        os.makedirs('24hr_Data/DNI', exist_ok=True)
        city_name = self.city_input.text()
        latitude, longitude = get_coordinates(city_name)

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
        
        print(f"Day number for {today} is {day_number}")

        # Check if the day_number is within the range of the DataFrame
        if day_number > len(city_df):
            raise ValueError("The day number exceeds the length of the data in KANPUR.csv")

        # Get the row for the calculated day number
        day_data = city_df.iloc[day_number - 1]  # Subtract 1 because DataFrame is 0-indexed

        # Convert the row data to a numpy array
        day_data_array = day_data.to_numpy()

        # Calculate the average of the values, ignoring zeros
        non_zero_values = day_data_array[day_data_array != 0]
        if len(non_zero_values) > 0:
            average_dni = np.mean(non_zero_values)
        else:
            average_dni = 0

        self.fetch_city_data = average_dni
        self.result_output.append(f"--> Got data for {city_name}. The optimal solar insolation value is {average_dni:.2f} Wh/m²/day.")
        self.unit_label.show()
        self.unit_input.show()
        self.area_label.show()
        self.area_input.show()
        self.area_button.show()


    def calculate_area_and_energy(self):
        unit = self.unit_input.currentText()
        area = float(self.area_input.text())
        area_in_square_meters = convert_area_to_square_meters(area, unit)
        if self.fetch_city_data:
            insolation = float(self.fetch_city_data)  # Replace with actual insolation data
            self.solar_energy = calculate_solar_energy(area_in_square_meters, insolation)
            self.result_output.append(f"--> Based on an area of {area} {unit} (~{area_in_square_meters:.2f} sq. meters), you can produce approximately {self.solar_energy:.2f} kWh of solar energy per day.")

            daily_usages = estimate_daily_usage(self.solar_energy)
            self.result_output.append("With this amount of energy, you can power (one of the following):")
            for usage in daily_usages:
                self.result_output.append(f"  - {usage}")

            self.rate_label.show()
            self.rate_input.show()
            self.calculate_button.show()
        else:
            self.result_output.append("Please fetch city data first.")

    def calculate_cost_savings(self):
        rate_per_kwh = float(self.rate_input.text())
        cost_savings = calculate_cost_savings(self.solar_energy, rate_per_kwh)
        self.result_output.append(f"You can save approximately Rs {cost_savings:.2f} per day on electricity.")
        self.result_output.append("Thank you!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app = App()
    app.show()
    sys.exit(app.exec_())
