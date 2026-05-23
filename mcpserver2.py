import requests
import os
from datetime import datetime
from fastmcp import FastMCP

mcp = FastMCP("TravelBuddy")

@mcp.tool()
def get_coordinates(city_name: str) -> str:
    """Find latitude and longitude for a city."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=1"
    response = requests.get(url)
    if response.status_code == 200 and response.json().get("results"):
        res = response.json()["results"][0]
        return f"City: {res['name']}, Lat: {res['latitude']}, Long: {res['longitude']}, Country: {res.get('country')}"
    return "City not found."

@mcp.tool()
def check_destination_weather(lat: float, lon: float) -> str:
    """Check if the current weather at coordinates is suitable for travel."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()["current_weather"]
        return f"It is currently {data['temperature']}°C with wind speeds of {data['windspeed']} km/h."
    return "Weather data unavailable."

@mcp.tool()
def travel_journal(action: str, content: str = "") -> str:
    """Save or read travel preferences and past trip notes. Action: 'save' or 'read'."""
    path = "travel_journal.txt"
    if action == "save":
        with open(path, "a") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d')}] {content}\n")
        return "Logged in your Travel Journal."
    else:
        if not os.path.exists(path): return "Journal is empty."
        with open(path, "r") as f: return f.read()

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)
