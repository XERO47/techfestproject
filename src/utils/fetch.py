import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.getenv('Weather_API_key')

def fetch_realtime_weather_data(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.text

<<<<<<< HEAD
def fetch_weather_forecast(location):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3"
    response = requests.get(url)
    return response.text
=======
def fetch_weather_forecast(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relativehumidity_2m,windspeed_10m"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.json())
>>>>>>> cf4b68a (changes)

