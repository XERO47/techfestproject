import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.getenv('Weather_API_key')

def fetch_realtime_weather_data(location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    response = requests.get(url)
    return response.text

def fetch_weather_forecast(location):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&days=3"
    response = requests.get(url)
    return response.text



