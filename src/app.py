## CLI version of the weather app
import sys
from utils import  get_weather, validate_args, get_emoji, get_temprature_emoji

def print_weather(city="Stockholm", weather=None):
    if weather is None:
        weather = get_weather(city)
    
    if weather.get('cod') == '404':
        print(f"Error: City '{city}' not found")
        return
        
    temp = weather['main']['temp']
    description = weather['weather'][0]['description']
    print(f"Weather Report for {city}:")
    print(f"{get_temprature_emoji(temp)}  Temperature: {temp}°C")
    print(f"{get_emoji(description)}  Conditions: {description.capitalize()} ")

    print(weather) # debug


def main():
    city = validate_args(sys.argv)

    #print(f"Getting weather for {city}") # debug
    print_weather(city=city)

    

if __name__ == "__main__":
    main()





