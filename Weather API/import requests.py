import sys
import requests
import csv
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
import random
from datetime import datetime

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Weather App')
        self.setGeometry(300, 300, 300, 250)

        layout = QVBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter a city name")
        layout.addWidget(self.city_input)

        self.get_weather_button = QPushButton('Get Temperature')
        self.get_weather_button.clicked.connect(self.get_city_temperature)
        self.get_weather_button.setStyleSheet("background-color: white; font-size: 14px; padding: 8px;")
        layout.addWidget(self.get_weather_button)

        self.get_random_city_button = QPushButton('Get Random City Temperature')
        self.get_random_city_button.clicked.connect(self.get_random_city_temperature)
        self.get_random_city_button.setStyleSheet("background-color: white; font-size: 14px; padding: 8px;")
        layout.addWidget(self.get_random_city_button)

        self.result_label = QLabel('')
        layout.addWidget(self.result_label)

        self.weather_icon = QLabel()
        self.weather_icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.weather_icon)

        self.setLayout(layout)

    def get_city_temperature(self):
        city = self.city_input.text()
        self.fetch_temperature(city)

    def get_random_city_temperature(self):
        cities = ["London", "Paris", "Berlin", "Madrid", "Rome", "Tokyo", "Sydney", "New York", "Moscow", "Beijing"]
        random_city = random.choice(cities)
        self.fetch_temperature(random_city)

    def fetch_temperature(self, city):
        api_key = "9fb9181a414242bb069ff4f7b4d97404"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()
            
            if self.data["cod"] == 200:
                temp_kelvin = self.data['main']["temp"]
                temp_celsius = temp_kelvin - 273.15
                self.result_label.setText(f"The temperature in {city} is {temp_celsius:.2f}°C")
                weather_condition = self.data['weather'][0]['main']
                self.update_weather_icon(weather_condition)
                self.save_to_csv(city, self.data)
            else:
                self.result_label.setText("Unable to fetch temperature data")
                self.weather_icon.clear()
        
        except requests.exceptions.RequestException as e:
            self.result_label.setText(f"An error occurred: {e}")
            self.weather_icon.clear()

    def update_weather_icon(self, weather_condition):
        icon_map = {
            "Clear": "☀️",
            "Clouds": "☁️",
            "Rain": "🌧️",
            "Snow": "❄️",
            "Thunderstorm": "⛈️",
            "Drizzle": "🌦️",
            "Mist": "🌫️"
        }
        icon = icon_map.get(weather_condition, "❓")
        self.weather_icon.setText(icon)
        self.weather_icon.setStyleSheet("font-size: 72px;")

    def save_to_csv(self, city, data):
        filename = 'weather_data.csv'
        fieldnames = ['timestamp', 'city', 'temperature', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity', 'weather_main', 'weather_description', 'wind_speed', 'wind_deg', 'clouds', 'country']
        
        file_exists = False
        try:
            with open(filename, 'r') as f:
                file_exists = True
        except FileNotFoundError:
            pass

        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            
            writer.writerow({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'city': city,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind']['deg'],
                'clouds': data['clouds']['all'],
                'country': data['sys']['country']
            })

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()

    # Set the application style
    app.setStyle("Fusion")

    # Set the color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(255, 255, 255))  # White background
    palette.setColor(QPalette.WindowText, QColor(0, 100, 0))  # Dark green text
    app.setPalette(palette)

    # Set the font to San Francisco (Mac's system font)
    font = QFont("SF Pro Text", 12)
    app.setFont(font)

    ex.show()
    sys.exit(app.exec_())
