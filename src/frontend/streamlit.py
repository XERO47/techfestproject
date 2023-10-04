import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt
import folium
import plotly.graph_objs as go
import requests
import json
from PIL import Image
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

unit = st.sidebar.selectbox("Unit", ["Celsius", "Fahrenheit"])
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
# st.write(weather_data)
try:
    if unit=="Fahrenheit":
        temp = weather_data['current']['temp_f']
        col1.metric("Temp", f"{temp} °F")
    else:
        temp = weather_data['current']['temp_c']
        col1.metric("Temp", f"{temp} °C")

    humidity = weather_data['current']['humidity']
    wind = weather_data['current']['wind_kph']

    col2.metric("Humidity", f"{humidity} %")
    col3.metric("Wind", f"{wind} kph")

    url = f'https:{weather_data["current"]["condition"]["icon"]}'
    image = Image.open(requests.get(url, stream=True).raw)

    col4.image(image, caption=f'{weather_data["location"]["name"]}')
    st.markdown(f'{weather_data["current"]["condition"]["text"]}')
except:
    st.error("No weather data available")


# ..............................Weather forecast graph...............................

if forecast:
    response = fetch_weather_forecast(f'{lat},{lng}')
    data = json.loads(response)
    st.write(data)
   
    # Parse the JSON response into a format that can be used by the Altair chart
    df = pd.DataFrame({
        "date": data["forecast"]["forecastday"][0]["hour"],
        "temp_max": [hour["temp_c"] for hour in data["forecast"]["forecastday"][0]["hour"]],
        "precipitation": [hour["precip_mm"] for hour in data["forecast"]["forecastday"][0]["hour"]],
        "weather": [hour["condition"]["text"] for hour in data["forecast"]["forecastday"][0]["hour"]]
    })

    # Define the color scale for the weather conditions
    scale = alt.Scale(
        domain=["Sunny", "Partly cloudy", "Cloudy", "Light rain", "Moderate rain", "Heavy rain", "Light snow", "Moderate snow", "Heavy snow"],
        range=["#FFD700", "#FFA500", "#A9A9A9", "#87CEFA", "#1E90FF", "#0000FF", "#FFFAFA", "#DCDCDC", "#808080"]
    )

    # Create the chart
    brush = alt.selection_interval(encodings=["x"])
    click = alt.selection_multi(encodings=["color"])
    points = (
        alt.Chart(df)
        .mark_point()
        .encode(
            alt.X("date:T", title="Date"),
            alt.Y(
                "temp_max:Q",
                title="Maximum Daily Temperature (C)",
                scale=alt.Scale(domain=[-5, 40]),
            ),
            color=alt.condition(brush, "weather:N", alt.value("lightgray"), scale=scale),
            size=alt.Size("precipitation:Q", scale=alt.Scale(range=[5, 200])),
        )
        .properties(width=550, height=300)
        .add_selection(brush)
        .transform_filter(click)
    )

    bars = (
        alt.Chart(df)
        .mark_bar()
        .encode( x="count()",
            y="weather:N",
            color=alt.condition(click, "weather:N", alt.value("lightgray"), scale=scale),
        )
        .transform_filter(brush)
        .properties(
            width=550,
        )
        .add_selection(click)
    )

    chart = alt.vconcat(points, bars, data=df, title=f"Weather Forecast for {data['location']['name']}")

    # Create Streamlit tabs for theme options
    # tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])
    # with tab1:
    #     st.altair_chart(chart, theme="streamlit", use_container_width=True)
    # with tab2:
    st.altair_chart(chart, theme=None, use_container_width=True)

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
