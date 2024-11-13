import sys
import requests

def get_api_key():
    return st.secrets["API_KEY"]

def get_api_url():
    api_url = st.secrets['WEATHER_API_URL']
    if not api_url:
        raise ValueError("WEATHER_API_URL environment variable is not set")
    return api_url

def get_api_params(city):
    return {
        "appid": get_api_key(),
        "q": city,
        "units": "metric",
    }

def validate_args(args):
    if len(args) < 2:
        print("Usage: python app.py <city>")
        sys.exit(1)
    return " ".join(args[1:])

def get_weather(city):
    response = requests.get(get_api_url(), params=get_api_params(city))
    return response.json()

def get_emoji(description):
    emoji = {
        "clear sky": "🌞",
        "clouds": "☁️",
        "rain": "🌧️",
        "rain and snow": "🌨️",
        "moderate rain": "🌧️",
        "snow": "❄️",
        "mist": "🌫️",
        "thunderstorm": "⛈️",
        "drizzle": "🌧️",
        "fog": "🌫️",
        "haze": "🌫️",
        "dust": "🌫️",
        "smoke": "🌫️",
        "broken clouds": "🌤️",
        "scattered clouds": "🌤️",
        "few clouds": "🌤️",
        "overcast clouds": "🌤️",
    }
    return emoji.get(description.lower(), "🌐")


def get_temprature_emoji(temp):
    if temp > 25:
        return "🔥"
    elif temp < 6:
        return "❄️"
    else:
        return "🌡️"
    
def get_wind_direction(wind_deg):
    if wind_deg is None:
        return "unknown"
    wind_directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = int((wind_deg / 45) + 0.5) % 8
    return wind_directions[index]

def make_weather_dict(city):
    weather = get_weather(city)
    
    temp = weather['main']['temp']
    wind_deg = weather['wind']['deg'] if weather.get('wind') else None
    wind_gust = weather['wind'].get('gust') if weather.get('wind') else None
    rain = weather['rain']['1h'] if weather.get('rain') else 0
    clouds = weather['clouds']['all'] if weather.get('clouds') else 0
    description = weather['weather'][0]['description']
    
    return {
        "temperature": temp,
        "feels_like": weather['main']['feels_like'],
        "humidity": weather['main']['humidity'],
        "pressure": weather['main']['pressure'],
        "wind_speed": weather['wind']['speed'],
        "wind_deg": wind_deg,
        "wind_direction": get_wind_direction(wind_deg),
        "wind_gust": wind_gust,
        "rain": rain,
        "clouds": clouds,
        "description": description,
        "emoji": get_emoji(description),
        "temperature_emoji": get_temprature_emoji(temp)
    }

