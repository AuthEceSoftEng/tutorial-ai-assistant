# pip install fastmcp
import requests
from fastmcp import FastMCP
from datetime import datetime

# Initialize the server
mcp = FastMCP("MyAssistantTools")

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """A simple tool to add two numbers together."""
    return a + b

@mcp.tool()
def get_time() -> dict:
    """Returns the current time with timezone offset."""
    local_dt = datetime.now().astimezone()
    return {
        "current_time": local_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "timezone": local_dt.strftime("%Z"),
        "utc_offset": local_dt.strftime("%z")
    }

@mcp.tool()
def get_coordinates(city_name: str) -> str:
    """Find the latitude and longitude for a given city name."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("results"):
        res = response.json()["results"][0]
        return f"City: {res['name']}, Lat: {res['latitude']}, Long: {res['longitude']}"
    return "City not found."

@mcp.tool()
def get_weather(latitude: float, longitude: float) -> str:
    """
    Get current weather using coordinates. 
    Note: AI should use a geocoding tool or its own knowledge to find lat/long.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true"
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()["current_weather"]
        return f"Temperature: {data['temperature']}°C, Windspeed: {data['windspeed']} km/h"
    return "Error fetching weather data."

if __name__ == "__main__":
    # Runs the server over stdio (Standard Input/Output)
    mcp.run(transport="http", host="127.0.0.1", port=8000)
