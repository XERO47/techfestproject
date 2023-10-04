import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import folium
import plotly.graph_objs as go
import requests
import json
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import geocoder
import sys
sys.path.append('../')

from src.utils.fetch import *

geolocator = Nominatim(user_agent="my_app")

# ...............................Style.............................................

st.markdown("""
<style>
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
iframe {
    height: 400px;
}
[data-testid="stSidebar"] {
    background-image: url(https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png);
    background-size: 200px;
    background-repeat: no-repeat;
    background-position: 4px 20px;
}
div.st-emotion-cache-13izhro {
    background-color: #FFFFFF;
    border: 1px solid #CCCCCC;
    padding: 5% 5% 5% 10%;
    border-radius: 5px;
    
    border-left: 0.5rem solid #9AD8E1 !important;
    box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
    
}  
button{
    width: 100%; !important;
}
</style>
""", unsafe_allow_html=True)


# .............................Sidebar..............................................


st.sidebar.title("Dashboard`version 0`")

def get_location_suggestions(location):
    suggestions = []
    if location:
        results = geolocator.geocode(location, exactly_one=False)
        for result in results:
            suggestions.append(result.address)
    return suggestions

location = st.sidebar.text_input("Location", key="location_input")
suggestions = get_location_suggestions(location)

if suggestions:
    location = st.sidebar.selectbox("Did you mean:", suggestions)

# unit = st.sidebar.selectbox("Unit", ["Celsius", "Fahrenheit"])
forecast = st.sidebar.toggle("Show Forecast")

if st.sidebar.button("Refresh"):
    # Clear the cache
    st.cache(allow_output_mutation=True)

# Set up the reminder
if st.sidebar.button("Set Reminder"):
    min_temp = st.sidebar.number_input("Minimum Temperature")
    max_temp = st.sidebar.number_input("Maximum Temperature")
    reminder = st.sidebar.text_input("Reminder Message")
    if min_temp and max_temp and reminder:
        if temp_min < min_temp or temp_max > max_temp:
            st.warning(reminder)

# ..................................ROWS.............................................

# Get the latitude and longitude of the location using the Nominatim API
if location:
    location = geolocator.geocode(location)
    lat = location.latitude
    lng = location.longitude
else:
    # Default to current location if no location is provided
    g = geocoder.ip('me')
    lat = g.latlng[0]
    lng = g.latlng[1]


# ..............................Metrics..............................................

st.markdown('### Metrics')
col1, col2, col3, col4 = st.columns(4)

response = fetch_realtime_weather_data(f'{lat},{lng}')
weather_data = json.loads(response)

try:
    temp = weather_data['data']['values']['temperature']
    rainProbablity = weather_data['data']['values']['precipitationProbability']
    wind_speed = weather_data['data']['values']['windSpeed']
    humidity = weather_data['data']['values']['humidity']

    col1.metric("Temp", f"{temp} °C")
    col3.metric("Humidity", f"{humidity}%")
    col4.metric("Wind Speed", f"{wind_speed}m/s")
    col2.metric("Rain Probablity", f"{rainProbablity}")
except:
    st.error("No weather data available")


# ..............................Weather forecast graph...............................

if forecast:
    response = fetch_weather_forecast(f'{lat},{lng}')
    data = json.loads(response)
    try:
        timestamps = []
        temperatures = []

        for minute in data['timelines']['minutely']:
            timestamps.append(minute['time'])
            temperatures.append(minute['values']['temperature'])

        df = pd.DataFrame({'Time': timestamps, 'Temperature': temperatures})
        df['Time'] = pd.to_datetime(df['Time'], unit='s')

        chart = st.line_chart(df.set_index('Time'), layout='wide', use_container_width=True, title='Temperature over time', line_width=2, color='red', opacity=0.8, x_axis_label='Time', y_axis_label='Temperature (°C)', legend=['Temperature'], font_color='blue', config={'displayModeBar': False, 'plotlyConfig': {'staticPlot': True}, 'backgroundColor': 'lightgray'})

    except:
        st.error("No graph available")

# ..............................Map................................................


m = folium.Map(location=[lat, lng], zoom_start=10)
folium.Marker(
    [lat,lng]
).add_to(m)
# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)


# .................................JsonFile Manupulation................................................

# Load the JSON file
with open('example.json', 'r') as f:
    data = json.load(f)

# Modify the data as needed
data['location']= f'{lat},{lng}'
data['max'] = 100
data['min'] = 0

# Save the modified data back to the file
with open('example.json', 'w') as f:
    json.dump(data, f)

# ...................................................................................

def genrate_alert(current_temp):
    pass
