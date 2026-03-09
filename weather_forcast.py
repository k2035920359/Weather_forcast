#!/usr/bin/env python
# coding: utf-8

import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import urllib3

urllib3.disable_warnings()

# Get the API key from the .env file
load_dotenv('.env', override=True)

api_key = os.getenv('WEATHER_API_KEY')
map_api_key = os.getenv('MAP_API_KEY')

#get datetime now
now = datetime.now()
print(now)

#Taipei location
lat = 25.04   
lon = 121.31

# Google Maps API
url_map = f"https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lon}&key={map_api_key}"
# Weather API
url_weather = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&cnt=1&lat={lat}&lon={lon}&appid={api_key}"

# Google Maps API response
map_response = requests.get(url_map)
map_data = map_response.json()

#wearther API response
weather_response = requests.get(url_weather, verify=False)
weather_data = weather_response.json()

# Print
address = map_data['results'][0]['formatted_address']

#print(weather_data)

temperature = weather_data['list'][0]['main']['temp']
feels_like = weather_data['list'][0]['main']['feels_like']
description = weather_data['list'][0]['weather'][0]['description']
wind_speed = weather_data['list'][0]['wind']['speed']
city = weather_data['city']['name']

# Print out the results
print(f"Location: {address}")
print(f"Temperature: {temperature}")
print(f"Feels Like: {feels_like}°C")
print(f"Weather Description: {description}")
print(f"Wind Speed: {wind_speed}")


# Weather report:
weather_string = f"""In {city}.
Temperature is {temperature}°C.
It feels like {feels_like}°C. 
Weather: {description}.
Wind speed: {wind_speed} m/s.
"""
print(weather_string)

#Use an LLM to plan your outfit
prompt = f"""Based on the following weather, 
suggest an appropriate outdoor outfit.

Forecast: {weather_string}
"""

# Print the LLM response
print(prompt)





