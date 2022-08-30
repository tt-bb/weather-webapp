from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import os


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city_name = request.form["city"]
    else:
        city_name = "Liège"

    # Get coordinates from city
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(city_name)

    # Get JSON
    key = os.environ['KEY']
    base_url = "https://api.openweathermap.org/data/2.5/onecall?"
    exclude = "minutely,hourly,alerts"
    url = f"{base_url}lat={location.latitude}&lon={location.longitude}&exclude={exclude}&appid={key}&units=metric"
    weather_data = requests.get(url).json()
    daily = weather_data["daily"]
    days = [((datetime.today() + timedelta(days=x)).strftime("%d-%m-%y")) for x in range(5)]

    # Print forecast for 5 days [FROM CLI SCRIPT]
    # for i in range(0, 5):
    #    feels_day = daily[i]["feels_like"]["day"]
    #    feels_night = daily[i]["feels_like"]["night"]
    #    weather = daily[i]["weather"][0]["main"]
    #    print(f"Forecast for : {days[i]}")
    #    print(f"\tFeels like day : {feels_day}°C")
    #    print(f"\tFeels like night : {feels_night}°C")
    #    print(f"\tWeather : {weather}")

    return render_template("index.html", city_name=city_name, days=days, daily=daily)


if __name__ == '__main__':
    app.run()