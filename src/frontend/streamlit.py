import streamlit as st
import matplotlib.pyplot as plt
# import pandas as pd
# from datetime import datetime, timedelta
# import pytz
import folium
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
    background-color: #f0f2f6;
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

unit = st.sidebar.selectbox("Unit", ["Celsius", "Fahrenheit"])
forecast = st.sidebar.checkbox("Show Forecast")

# Set up the reminder
if st.sidebar.button("Set Reminder"):
    min_temp = st.sidebar.number_input("Minimum Temperature")
    max_temp = st.sidebar.number_input("Maximum Temperature")
    reminder = st.sidebar.text_input("Reminder Message")
    if min_temp and max_temp and reminder:
        if temp_min < min_temp or temp_max > max_temp:
            st.warning(reminder)

# ..................................ROWS.............................................


# Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Max", "70 °F", "1.2 °F")
col2.metric("Min", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

# Row B
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

# Map
m = folium.Map(location=[lat, lng], zoom_start=10)
folium.Marker(
    [lat,lng]
).add_to(m)
# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)


# ..............................Weather forecast graph.............................

if forecast:
    response = fetch_weather_forecast(f'{lat},{lng}')
    data = json.loads(response)

    timestamps = []
    temperatures = []

    for minute in data['timelines']['minutely']:
        timestamps.append(minute['time'])
        temperatures.append(minute['values']['temperature'])

    fig, ax = plt.subplots()
    ax.plot(timestamps, temperatures)
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    ax.set_title(f'Temperature Forecast for {(geolocator.reverse(f"{lat}, {lng}")).address}')

    st.pyplot(fig)



# .................................................................................

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
