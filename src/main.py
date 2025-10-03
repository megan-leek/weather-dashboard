
import pandas as pd
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load crags from CSV
crags = pd.read_csv("data/crags.csv").to_dict(orient="records")
load_dotenv()
api_key = os.getenv("OWM_API_KEY")

if not api_key:
    raise ValueError("❌ OWM_API_KEY not found. Check your .env file or GitHub Secrets.")
# print(f"🔑 API Key loaded: {api_key}")
 # Replace with your actual OpenWeatherMap key

def log_weather():
    records = []
    for crag in crags:
        lat, lon = crag["lat"], crag["lon"]
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            rain = data.get("rain", {}).get("1h", 0)
            desc = data["weather"][0]["description"]
            records.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "crag": crag["name"],
                "lat": lat,
                "lon": lon,
                "rain_mm": rain,
                "description": desc
            })
        else:
            print(f"Error for {crag['name']}: {response.status_code} - {response.text}")

    df = pd.DataFrame(records)
    log_path = "data/rain_log.csv"
    file_exists = os.path.isfile(log_path)
    df.to_csv(log_path, mode="a", header=not file_exists, index=False)
    print(f"✅ Logged weather at {datetime.now().strftime('%H:%M')}")

if __name__ == "__main__":
    log_weather()

import sys
with open("data/env_check.txt", "a") as f:
    f.write(f"{sys.executable} @ {datetime.now()}\n")