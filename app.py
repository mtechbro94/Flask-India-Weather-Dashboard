from flask import Flask, render_template, request
import requests
import json
import os
from datetime import datetime

app = Flask(__name__)


# Set your OpenWeatherMap API key here (or use environment variable)
API_KEY = os.getenv("OPENWEATHER_API_KEY", "WEATHER_API_KEY")

# Load Indian cities from JSON (extract city names for dropdown)
with open("static/indian_cities.json", "r", encoding="utf-8") as f:
    city_data = json.load(f)
    indian_cities = [city["city"] for city in city_data]

@app.route("/", methods=["GET", "POST"])
def index():

    weather_data = None
    forecast_data = None
    selected_city = None
    error_message = None
    current_date = datetime.now().strftime("%A, %d %B %Y %I:%M %p")

    if request.method == "POST":
        selected_city = request.form.get("city")
        if selected_city:
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
                    from collections import OrderedDict
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

    return render_template(
        "index.html",
        cities=indian_cities,
        weather=weather_data,
        forecast=forecast_data,
        selected_city=selected_city,
        error=error_message
    )

if __name__ == "__main__":
    app.run(debug=True)
