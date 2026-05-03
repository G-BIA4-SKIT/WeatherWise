import requests
from config import WEATHER_API_KEY

def validate_weather_key():
    if not WEATHER_API_KEY:
        raise ValueError("Missing weather API key. Add WEATHER_API_KEY to the .env file.")

def get_weather(city, day):
    validate_weather_key()

    try:
        if day == "Today":
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": WEATHER_API_KEY, "units": "imperial"}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            return {
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "condition": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"]
            }

        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {"q": city, "appid": WEATHER_API_KEY, "units": "imperial"}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "list" not in data or len(data["list"]) < 9:
            raise ValueError("Not enough forecast data available for tomorrow.")

        entry = data["list"][8]

        return {
            "temp": entry["main"]["temp"],
            "feels_like": entry["main"]["feels_like"],
            "condition": entry["weather"][0]["description"],
            "humidity": entry["main"]["humidity"],
            "wind_speed": entry["wind"]["speed"]
        }

    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            return None
        if response.status_code == 401:
            raise ValueError("Invalid weather API key.")
        raise