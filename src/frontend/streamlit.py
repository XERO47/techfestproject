import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import pytz
import folium

api_key = "5b5af7a943581522b1aa5ef1102ef5e9"

# Set up the sidebar
st.sidebar.header("Settings`version 0`")
location = st.sidebar.text_input("Location", "London, UK")
unit = st.sidebar.selectbox("Unit", ["Celsius", "Fahrenheit"])
forecast = st.sidebar.checkbox("Show Forecast")

# Add a global map
st.title("Global Temperature Map")
m = folium.Map()
folium.TileLayer(
    tiles="https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid={api_key}",
    attr="OpenWeatherMap",
    name="Temperature Map",
    overlay=True,
).add_to(m)
st.write(m._repr_html_(), unsafe_allow_html=True)

# Add a chart
st.title("Temperature Over Time")
start_time = datetime.now(pytz.utc) - timedelta(hours=24)
end_time = datetime.now(pytz.utc)
url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={data['coord']['lat']}&lon={data['coord']['lon']}&start={int(start_time.timestamp())}&end={int(end_time.timestamp())}&appid={api_key}&units=metric"
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data['hourly'])
df['dt'] = pd.to_datetime(df['dt'], unit='s')
df.set_index('dt', inplace=True)
if unit == "Fahrenheit":
    df = df.apply(lambda x: (x * 9/5) + 32)
st.line_chart(df['temp'])

# Add CSS styling
st.markdown("""
<style>
body {
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)

# Set up the reminder
if st.sidebar.button("Set Reminder"):
    min_temp = st.sidebar.number_input("Minimum Temperature")
    max_temp = st.sidebar.number_input("Maximum Temperature")
    reminder = st.sidebar.text_input("Reminder Message")
    if min_temp and max_temp and reminder:
        if temp_min < min_temp or temp_max > max_temp:
            st.warning(reminder)

# Show forecast
if forecast:
    st.title("Weather Forecast")
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    for forecast in data['list']:
        dt = datetime.fromtimestamp(forecast['dt'])
        if dt.hour == 12:
            st.write(
                f"{dt.strftime('%A %B %d %Y')}: {forecast['weather'][0]['description']}, {forecast['main']['temp']}°{unit[0]}")
