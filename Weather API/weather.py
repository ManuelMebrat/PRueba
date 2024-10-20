import sys
import requests 
from PyQt5.QtWidgets import (QApplication,QLabel,QPushButton,
                             QWidget,QLineEdit,QVBoxLayout)
import json
from PyQt5.QtCore import Qt
import random 

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.city_label = QLabel("Enter a cityname",self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get weather",self)
        self.get_random_city_button = QPushButton("Random City",self)
        self.temp_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.city_label_name = QLabel(self)
    
        self.initUI() 
        


    def initUI(self):
        #Definimos titulo
        self.setWindowTitle("WeatherAPP")
        #alineamos verticalmente
        vbox = QVBoxLayout() 

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.get_random_city_button)
        vbox.addWidget(self.city_label_name)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        
        

        self.setLayout(vbox)

        #Alineamos en el centro
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.city_label_name.setAlignment(Qt.AlignCenter)
       

        #definimos como objetos para aplicar CSS
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temp_label.setObjectName("temp_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.city_label_name.setObjectName("city_label_name")
        self.get_random_city_button.setObjectName("get_random_city_button")
        


        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: darkgreen;
            }
                        
            QLabel, QPushButton{
                
                font-family: calibry;  }
                        
            QLabel#city_label{
                font-size:40px;
                font-style:italic;

                font-weight:bold;
                           
                           } 
            
            QLabel#temp_label{
                           
                font-size:70px;
  
                           
                           }
            QLabel#city_label_name{
                
                font-size:40px;
                font-style:italic;
                           
                           }

            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;        
                           
                           }

            QLabel#description_label{
                font-size: 50px;
                           }

            QLineEdit#city_input{
                background-color: lightgreen;
                font-size:20px;
                font-style:italic;
                color: black;  
                padding: 5px;  

                           }

            QPushButton#get_weather_button{
                border: 2px solid darkgreen;
                font-size:30px;
                font-weight:bold;
                           
                           }

            QPushButton#get_random_city_button
                           {
                border: 2px solid darkgreen;
                font-size:20px;
                font-weight:bold;
                                    }
                """)
        
        self.get_weather_button.clicked.connect(self.get_weather) #connect nuestro boton al metood de abajo
        self.get_random_city_button.clicked.connect(self.get_random_city) #connect nuestro boton al metood de abajo

    def get_weather(self):

        city = self.city_input.text()
        self.fetch_weather_date(city)
        
    def get_random_city(self):

        cities = ["London", "Paris", "Berlin", "Madrid", "Rome", "Tokyo", "Sydney", "Vienna", "Budapest", "Moscow", "Beijing", "Shanghai", "Istanbul", "Cairo", "Miami", "New York", "Los Angeles", "Chicago", "Houston", "Philadelphia", "Atlanta", "Washington DC", "Boston", "San Francisco", "Seattle", "Denver", "San Diego", "San Jose", "Austin", "Santa Fe", "Portland", "Oregon", "Sacramento", "San Francisco", "Los Angeles", "San Diego", "San Jose", "Phoenix", "Mesa", "Albuquerque", "Las Vegas", "Reno", "Salt"]
        city = random.choice(cities)
        self.fetch_weather_date(city)


    def fetch_weather_date(self,city,):
     
        api_key = "9fb9181a414242bb069ff4f7b4d97404"
    
        url =f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            self.data = response.json()

            if self.data["cod"] == 200:
                self.display_weather(self.data)
                self.save_data(self.data)

        except requests.exceptions.HTTPError as HTTPERORR:
            match response.status_code:
                case 400:
                    self.display_error("Bad request: \n Please check your  input")
                case 401:
                    self.display_error("Unautorized: \n invalid APIkey")
                case 403:
                    self.display_error("forbidden: \n access deny ")
                case 404:
                    self.display_error("Not found: \n city not found")
                case 500:
                    self.display_error("Internal server error: \n try later")
                case 502:
                    self.display_error("Badgateway: \n invalid response from the server")
                case 503:
                    self.display_error("Service unavailable: \n server is down")
                case 504:
                    self.display_error("gateway timeout: \n no response form the server")
                case _:
                    self.display_error (f"http eroror ocurred: \n {HTTPERORR}")
               
            
        except  requests.exceptions.ConnectionError:
            print("connection error \n Check your connection")
        except requests.exceptions.Timeout:
            print("time our error \n Be faster")
        except requests.exceptions.TooManyRedirects:
            print("Too many redirects \n check url")
        except requests.exceptions.RequestException as req_error:
            print(f"Request error {req_error}")





    def display_error(self,message):
        self.temp_label.setStyleSheet("font-size:30px;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temp_label.setStyleSheet("font-size:75px;")

        temp_kelvin = data['main']["temp"]
        temp_kelvin = temp_kelvin - 273.15
        weather_description = data['weather'][0]['description']

        weather_id = data['weather'][0]['id']
        city_name = data['name']

        self.temp_label.setText(f"{temp_kelvin:.0f}℃")

        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")
        self.city_label_name.setText(f"{city_name}")

  
        
    
    

        



    def display_error(self,message):
        self.temp_label.setStyleSheet("font-size:30px;")
        self.temp_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temp_label.setStyleSheet("font-size:75px;")

        temp_kelvin = data['main']["temp"]
        temp_kelvin = temp_kelvin - 273.15
        weather_description = data['weather'][0]['description']

        weather_id = data['weather'][0]['id']
        city_name = data['name']

        self.temp_label.setText(f"{temp_kelvin:.0f}℃")

        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(f"{weather_description}")
        self.city_label_name.setText(f"{city_name}")


    @staticmethod
    def get_weather_emoji(weather_id):
        
        if  200 <= weather_id <= 232:
                return "🌩️"
        elif 300 <= weather_id <= 321:
                return "☁️"
        elif 500 <= weather_id <= 531:
                return "🌧️"
        elif 600 <= weather_id <= 622:
                return "❅"
        elif 701 <= weather_id <= 741:
                return "🌫️"
        elif 702 == weather_id:
             return "🌋"
        elif 771 == weather_id:
             return "🌬️"
        elif 781 == weather_id:
             return "🌪️"
        elif 800 == weather_id:
             return "☀️"
        elif 801 <= weather_id <=804:
             return "🌥️"
    def save_data(self, data):
        try:
            # Intenta abrir y leer el archivo JSON existente
            with open('weather_data.json', 'r') as f:
                weather_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Si el archivo no existe o está vacío, inicia una lista vacía
            weather_data = []

        # Añade el nuevo registro de clima al final de la lista
        weather_data.append(data)

        # Escribe toda la lista de vuelta al archivo JSON
        with open('weather_data.json', 'w') as f:
            json.dump(weather_data, f, indent=4)
        
        print("Data saved to weather_data.json")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

