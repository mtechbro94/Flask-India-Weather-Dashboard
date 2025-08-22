import streamlit as st
import requests
import json
import os
from datetime import datetime
from collections import OrderedDict

# Set your OpenWeatherMap API key here (or use environment variable)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "93db53cf4d61827af7b9242e4eb9c0c2")

# Load Indian cities from JSON (extract city names for dropdown)
with open("static/indian_cities.json", "r", encoding="utf-8") as f:
    city_data = json.load(f)
    indian_cities = [city["city"] for city in city_data]

st.set_page_config(page_title="India Weather Dashboard", layout="centered")
st.title("🇮🇳 India Weather Dashboard")

st.markdown("Get real-time weather and 5-day forecast for Indian cities.")

selected_city = st.selectbox("Select a city:", sorted(indian_cities))

if st.button("Get Weather"):
    weather_data = None
    forecast_data = None
    error_message = None
    current_date = datetime.now().strftime("%A, %d %B %Y %I:%M %p")

    # Current weather
    url = f"https://api.openweathermap.org/data/2.5/weather?q={selected_city},IN&appid={API_KEY}&units=metric"
    # 5-day forecast
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={selected_city},IN&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        forecast_resp = requests.get(forecast_url, timeout=10)
        forecast_json = forecast_resp.json()

        if data.get("cod") == 200:
            weather_data = {
                "city": selected_city,
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "pressure": data["main"]["pressure"],
                "wind_speed": data["wind"]["speed"],
                "description": data["weather"][0]["description"].capitalize(),
                "date": current_date
            }
        else:
            error_message = data.get("message", "Could not fetch weather data.")

        # Parse 5-day forecast (group by day, pick noon forecast for each day)
        if forecast_json.get("cod") == "200":
            forecast_days = OrderedDict()
            for entry in forecast_json["list"]:
                dt_txt = entry["dt_txt"]
                date_str = dt_txt.split(" ")[0]
                time_str = dt_txt.split(" ")[1]
                # Pick 12:00:00 forecast for each day
                if time_str == "12:00:00":
                    forecast_days[date_str] = {
                        "date": datetime.strptime(date_str, "%Y-%m-%d").strftime("%A, %d %b"),
                        "temp": entry["main"]["temp"],
                        "desc": entry["weather"][0]["description"].capitalize(),
                        "icon": entry["weather"][0]["icon"]
                    }
            # Only next 5 days
            forecast_data = list(forecast_days.values())[:5]
        else:
            forecast_data = None
    except Exception as e:
        error_message = f"Error: {str(e)}"

    if error_message:
        st.error(error_message)
    if weather_data:
        st.subheader(f"Current Weather in {weather_data['city']}")
        st.write(f"**{weather_data['description']}**")
        st.metric("Temperature (°C)", weather_data["temperature"])
        st.metric("Feels Like (°C)", weather_data["feels_like"])
        st.metric("Humidity (%)", weather_data["humidity"])
        st.metric("Pressure (hPa)", weather_data["pressure"])
        st.metric("Wind Speed (m/s)", weather_data["wind_speed"])
        st.caption(weather_data["date"])
    if forecast_data:
        st.subheader("5-Day Forecast")
        for day in forecast_data:
            col1, col2 = st.columns([1, 3])
            with col1:
                st.image(f"http://openweathermap.org/img/wn/{day['icon']}@2x.png", width=60)
            with col2:
                st.write(f"**{day['date']}**: {day['temp']}°C, {day['desc']}")
