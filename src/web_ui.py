import streamlit as st
import folium
from streamlit_folium import st_folium

from utils import get_weather, get_emoji, get_temprature_emoji, get_wind_direction, make_weather_dict

def write_weather(city):
    # Make weather dictionary
    weather_dict = make_weather_dict(city)
    
    # Add subheading
    st.subheader(f"Weather Report for {city}")


    # Create two columns
    col1, col2 = st.columns(2)
    
    # Column 1
    with col1:
        st.write(f"{get_temprature_emoji(weather_dict['temperature'])}  Temperature: {weather_dict['temperature']}°C (feels like {weather_dict['feels_like']}°C)")
        st.write(f"{get_emoji(weather_dict['description'])}  Conditions: {weather_dict['description'].capitalize()} ")
        st.write(f"💧  Rain: {weather_dict['rain']} mm")
        st.write(f"🧭  Wind direction: {get_wind_direction(wind_deg=weather_dict['wind_deg'])}")
    
    # Column 2
    with col2:
        st.write(f"💧  Humidity: {weather_dict['humidity']}%")
        st.write(f"🗜  Pressure: {weather_dict['pressure']} hPa")
        st.write(f"☁️  Clouds: {weather_dict['clouds']}%")
        st.write(f"💨  Wind speed: {weather_dict['wind_speed']} m/s (gust: {weather_dict['wind_gust'] if weather_dict['wind_gust'] else 'unknown'} m/s)")


def write_error(city):
    st.error(f"Error: City '{city}' not found")


def show_map(city, weather):
    # Add subheading
    st.subheader(f"Map for {city}")

    lat = weather['coord']['lat']
    long = weather['coord']['lon']
    # Initialize map
    m = folium.Map(location=[lat, long], zoom_start=5)

    # Add a marker with temperature in the tooltip
    temp = weather['main']['temp']
    folium.Marker([lat, long], tooltip=f"{city}: {temp}°C").add_to(m)

    # Display map in Streamlit
    st_folium(m, width=700, height=500)

def main():
    st.title("Weather App")

    city = st.text_input("Enter a city", "Stockholm")
    weather = get_weather(city)

    if weather.get('cod') != '404':
        write_weather(city)
        show_map(city, weather)
    else:
        write_error(city)



if __name__ == "__main__":
    main()