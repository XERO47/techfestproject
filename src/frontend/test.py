import streamlit as st
import requests

api_key = "5b5af7a943581522b1aa5ef1102ef5e9"

location = st.text_input("Location", "London, UK")

url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
response = requests.get(url)
data = response.json()
st.write(data)