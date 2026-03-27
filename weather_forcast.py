#!/usr/bin/env python
# coding: utf-8

import os
import requests
from google import genai
from dotenv import load_dotenv
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



# Get the API key from the .env file
load_dotenv('.env', override=True)
api_key = os.getenv('WEATHER_API_KEY')
map_api_key = os.getenv('MAP_API_KEY')
gemini_key = os.getenv('GEMINI_API_KEY')


# Configure the Gemini API
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

#get datetime now
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"Current Time: {now}")

#Taipei location
location_name = "臺北市"

def get_cwa_weather(api_key, location_name):
    # Weather API
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={api_key}&locationName={location_name}"

    try:
        #wearther API response
        weather_response = requests.get(url, verify=False)
        weather_data = weather_response.json()
        print(weather_data)

        if weather_response.status_code != 200:
            #print(weather_data)
            location_data = data['records']['location'][0]
            weather_elements = location_data['weatherElement']
            
            # 提取關鍵資訊 (抓取最近的一個時段 index 0)
            # Wx: 天氣現象, MaxT: 最高溫, MinT: 最低溫, PoP: 降雨機率, CI: 舒適度
            weather_desc = weather_elements[0]['time'][0]['parameter']['parameterName']
            pop = weather_elements[1]['time'][0]['parameter']['parameterName'] # 降雨機率
            min_t = weather_elements[2]['time'][0]['parameter']['parameterName']
            comfort = weather_elements[3]['time'][0]['parameter']['parameterName']
            max_t = weather_elements[4]['time'][0]['parameter']['parameterName']


            # Print out the results
            weather_summary = (
                f"地點: {location_name}\n"
                f"天氣狀況: {weather_desc}\n"
                f"氣溫範圍: {min_t}°C - {max_t}°C\n"
                f"降雨機率: {pop}%\n"
                f"體感舒適度: {comfort}"
            )
            print(weather_summary)
        else:
            print(f"Error fetching weather data: {weather_data.get('message')}")
    except Exception as e:
        print(f"An error occurred: {e}")


weather_info = get_cwa_weather(api_key=api_key, location_name=location_name)
print(f"Weather forcast: {weather_info}\n")

prompt = f"""Based on the following weather, 
    suggest an appropriate outdoor outfit.

    Forecast: {weather_info}

    Recommendation: """

# Print the LLM response
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents={prompt}
)
print("\nOutfit Recommendation:")
print(response.text)
print(response.model_dump_json(
    exclude_none=True, indent=4))






