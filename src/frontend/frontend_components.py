import sys
sys.path.append('src')
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import altair as alt
import folium
import requests
import json
from PIL import Image
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
import geocoder



from utils.fetch import *


geolocator = Nominatim(user_agent="my_app")

def main():

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

    if st.sidebar.button("Refresh"):
        st.cache(allow_output_mutation=True)


    # Set up the reminder

    min_temp = st.sidebar.slider("Minimum Temperature")
    max_temp = st.sidebar.slider("Maximum Temperature")
    email = st.sidebar.text_input("Want alert in your inbox?")
    if st.sidebar.button("Set Reminder"):
        if min_temp and max_temp and email:
            read_write_file('agent1qfu86j53jq_data.json')
            st.success("Reminder set successfully!")
        else:
            st.error("Failed to set reminder.")

        


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

    # Load the JSON file
    def read_write_file(file)
        with open('file', 'r') as f:
            data = json.load(f)

        # Modify the data as needed
        data['lat'].append(f'{lat}')
        data['lon'].append(f'{lng}')
        data['max'].append(f'{max_temp}')
        data['min'].append(f'{min_temp}')
        data['status'].append('active')
    
        # Save the modified data back to the file
        with open('file', 'w') as f:
            json.dump(data, f)


    # ..............................Metrics..............................................

    st.markdown('### Metrics')
    col1, col2, col3, col4 = st.columns(4)

    response = fetch_realtime_weather_data(f'{lat},{lng}')
    weather_data = json.loads(response)

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
        st.write(f'Last updated: {weather_data["current"]["last_updated"]}   |   {weather_data["current"]["condition"]["text"]}')
    except:
        st.error("No weather data available")


    # ..............................Weather forecast graph...............................

    try:
        response = fetch_weather_forecast(f'{lat},{lng}')
        data = json.loads(response)

        # Parse the JSON response into a format that can be used by the Altair chart
        df = pd.DataFrame({
            "date":[time['time'] for time in data["forecast"]["forecastday"][0]["hour"]],
            "temp_max": [hour["temp_c"] for hour in data["forecast"]["forecastday"][0]["hour"]],
            "precipitation": [hour["precip_mm"] for hour in data["forecast"]["forecastday"][0]["hour"]],
            "weather": [hour["condition"]["text"] for hour in data["forecast"]["forecastday"][0]["hour"]],
            "wind_speed": [hour["wind_kph"] for hour in data["forecast"]["forecastday"][0]["hour"]],
            "rain_chance": [hour["chance_of_rain"] for hour in data["forecast"]["forecastday"][0]["hour"]],
        })

        # Define the color scale for the weather conditions
        scale = alt.Scale(
            domain=["Sunny","Partly cloudy","Clear","Patchy rain possible","Moderate rain","Mist"],
            range=["#e7ba52", "#aec7e8", "#1f77b4", "#a7a7a7", "#9467bd", "#8c564b"],
        )
        color = alt.Color("weather:N", scale=scale)

        # Create the chart
        brush = alt.selection_interval(encodings=["x"])
        click = alt.selection_point(encodings=["color"])

        points = (
            alt.Chart(df)
            .mark_point(size=200)
            .encode(
                alt.X("date:T", title="Today", axis=alt.Axis(format="%H:%M")),
                alt.Y(
                    "temp_max:Q",
                    title="Maximum Daily Temperature (C)",
                    scale=alt.Scale(domain=[-5, 40]),
                ),
                color=alt.condition(brush, color, alt.value("lightgray")),
                tooltip=[
                alt.Tooltip("date:T", title="Date"),
                alt.Tooltip("temp_max:Q", title="Maximum Temperature (C)"),
                alt.Tooltip("wind_speed:Q", title="Wind Speed (kph)"),
                alt.Tooltip("weather:N", title="Weather"),
                alt.Tooltip("precipitation:Q", title="Precipitation"),
                alt.Tooltip("rain_chance:Q", title="Rain Chance"),
                ],
            )
            .properties(width=550, height=300)
            .add_params(brush)
            .transform_filter(click)
        )

        bars = (
            alt.Chart(df)
            .mark_bar()
            .encode(
                x="count()",
                y="weather:N",
                color=alt.condition(click, color, alt.value("lightgray")),
            )
            .transform_filter(brush)
            .properties(
                width=550,
            )
            .add_params(click)
        )

        chart = alt.vconcat(points, bars, data=df, title=f"Weather Forecast for {data['location']['name']}")

        tab1, tab2 = st.tabs(["Chart", "Data"])

        with tab1:
            st.altair_chart(chart, theme=None, use_container_width=True)
        with tab2:
            st.write(df)
    except:
        st.error("No weather forecast data available")

    # ..............................Map................................................


    m = folium.Map(location=[lat, lng], zoom_start=10)
    folium.Marker(
        [lat,lng]
    ).add_to(m)
    # call to render Folium map in Streamlit
    st_data = st_folium(m, width=725)


    # ...................................................................................

def generate_alert(current_temp):
    st.warning(f"Current temperature is {current_temp} °C")
    
if __name__ == "__main__":
    main()