import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.getenv('Weather_API_key')

def fetch_realtime_weather_data(location):
    url = f"https://api.tomorrow.io/v4/weather/realtime?location={location}&apikey={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)

def fetch_weather_forecast(location):
    url = f"https://api.tomorrow.io/v4/weather/forecast?location={location}&apikey={api_key}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return(response.text)

