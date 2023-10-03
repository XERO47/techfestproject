import streamlit as st
# import pandas as pd
# from datetime import datetime, timedelta
# import pytz
import folium
import json
from fetch import *
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

geolocator = Nominatim(user_agent="my_app")
api_key = "5b5af7a943581522b1aa5ef1102ef5e9"

st.set_page_config(layout='wide', initial_sidebar_state='expanded')


# ...............................Style.............................................

st.markdown("""
<style>
body {
    background-color: #f0f2f6;
}
iframe {
    height: 400px;
}
.st-emotion-cache-a2tkzm {
    width: 100%;
}     
</style>
""", unsafe_allow_html=True)

# ..................................................................................



# ..................................................................................

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

# ...............................................................................


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
    # Default to London, UK if no location is provided
    lat, lng = 51.5074, -0.1278

# Map
m = folium.Map(location=[lat, lng], zoom_start=10)
folium.Marker(
    [lat,lng]
).add_to(m)
# call to render Folium map in Streamlit
st_data = st_folium(m, width=725)



# Add a chart
# st.title("Temperature Over Time")
# start_time = datetime.now(pytz.utc) - timedelta(hours=24)
# end_time = datetime.now(pytz.utc)
# url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={data['coord']['lat']}&lon={data['coord']['lon']}&start={int(start_time.timestamp())}&end={int(end_time.timestamp())}&appid={api_key}&units=metric"
# response = requests.get(url)
# data = response.json()
# df = pd.DataFrame(data['hourly'])
# df['dt'] = pd.to_datetime(df['dt'], unit='s')
# df.set_index('dt', inplace=True)
# if unit == "Fahrenheit":
#     df = df.apply(lambda x: (x * 9/5) + 32)
# st.line_chart(df['temp'])




# Set up the reminder
if st.sidebar.button("Set Reminder"):
    min_temp = st.sidebar.number_input("Minimum Temperature")
    max_temp = st.sidebar.number_input("Maximum Temperature")
    reminder = st.sidebar.text_input("Reminder Message")
    if min_temp and max_temp and reminder:
        if temp_min < min_temp or temp_max > max_temp:
            st.warning(reminder)



# Load the JSON file
with open('example.json', 'r') as f:
    data = json.load(f)

# Modify the data as needed
data['latitude'] = lat
data['longitude'] = lng
data['max'] = 0
data['min'] = 0

# Save the modified data back to the file
with open('example.json', 'w') as f:
    json.dump(data, f)
# Show forecast
# if forecast:
#     st.title("Weather Forecast")
#     url = f"https://api.openweathermap.org/data/2.5/forecast?q={location}&appid={api_key}&units=metric"
#     response = requests.get(url)
#     data = response.json()
#     for forecast in data['list']:
#         dt = datetime.fromtimestamp(forecast['dt'])
#         if dt.hour == 12:
#             st.write(
#                 f"{dt.strftime('%A %B %d %Y')}: {forecast['weather'][0]['description']}, {forecast['main']['temp']}°{unit[0]}")

