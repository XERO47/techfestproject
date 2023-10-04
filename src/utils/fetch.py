import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.getenv('Weather_API_key')

<<<<<<< HEAD
def fetch_realtime_weather_data(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.json())

def fetch_weather_forecast(location):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)

print(fetch_realtime_weather_data(18.51,73.85))
=======
def fetch_realtime_weather_data(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.text

def fetch_weather_forecast(location):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3"
    response = requests.get(url)
    return response.text

>>>>>>> ccfd40d (updated code)
