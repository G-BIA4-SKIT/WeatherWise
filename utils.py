def format_weather_summary(weather):
    return (
        f"{weather['condition'].title()} | {weather['temp']}°F "
        f"(feels like {weather['feels_like']}°F) | "
        f"Humidity: {weather['humidity']}% | Wind: {weather['wind_speed']} mph"
    )