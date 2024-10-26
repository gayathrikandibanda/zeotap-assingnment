import requests
import time
from datetime import datetime
from statistics import mean

# Your API key
API_KEY = "b208ca92e1d48d866aa15b95a502ae3b"
# List of cities you want to monitor
CITIES = ["Delhi", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Hyderabad"]
API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}"

# Convert temperature from Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Get weather data from OpenWeatherMap API
def get_weather_data(city):
    try:
        # Properly format the API URL with the city name and API key
        response = requests.get(API_URL.format(city, API_KEY))
        
        # Print status code and raw response to diagnose the issue
        print(f"API Response for {city}: {response.status_code}")  # Status code
        print(f"API Raw Response for {city}: {response.text}")  # Raw response text

        response.raise_for_status()  # Raise exception for 4xx/5xx status codes

        # Correct the content type check to handle cases with charset
        if response.headers['Content-Type'].startswith('application/json'):
            data = response.json()  # Parse the response to JSON
            return {
                "city": city,
                "temp": kelvin_to_celsius(data["main"]["temp"]),
                "feels_like": kelvin_to_celsius(data["main"]["feels_like"]),
                "condition": data["weather"][0]["main"],
                "timestamp": data["dt"]
            }
        else:
            print(f"Unexpected content type: {response.headers['Content-Type']}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"Error decoding JSON: {json_err}")
    return None

# Monitor weather in real-time (e.g., every 5 minutes)
def monitor_weather(interval=300):
    daily_data = {city: [] for city in CITIES}  # Weather data for each city
    start_time = datetime.now().date()

    while True:
        for city in CITIES:
            data = get_weather_data(city)
            if data:
                daily_data[city].append(data)
                print(f"Weather in {city}: {data}")  # Print current weather
            
            # If it's a new day, summarize the previous day's data
            if datetime.now().date() != start_time:
                for city in CITIES:
                    summary = daily_weather_summary(daily_data[city])
                    print(f"Daily Summary for {city}: {summary}")
                daily_data = {city: [] for city in CITIES}  # Reset for the new day
                start_time = datetime.now().date()

        time.sleep(interval)  # Wait for the next interval

# Aggregate and rollup the daily weather data
def daily_weather_summary(weather_data):
    temps = [entry["temp"] for entry in weather_data]
    dominant_condition = max(set([entry["condition"] for entry in weather_data]), 
                             key=lambda cond: [entry["condition"] for entry in weather_data].count(cond))
    return {
        "average_temp": mean(temps),
        "max_temp": max(temps),
        "min_temp": min(temps),
        "dominant_condition": dominant_condition
    }

# Test the system with a single city and shorter interval (for testing purposes)
if __name__ == "__main__":
    # Monitor with a shorter interval (10 seconds for testing)
    monitor_weather(interval=10)
