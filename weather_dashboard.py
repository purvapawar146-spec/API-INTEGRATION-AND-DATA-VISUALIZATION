import requests
import matplotlib.pyplot as plt
import datetime
import pandas as pd
import seaborn as sns

# ---- SETTINGS ----
API_KEY = "6b70b0a7231809b69402f68d0b0e923f"  # <-- Replace with your OpenWeatherMap API key
CITY = "Mumbai"  # You can change this to any city
NUM_DAYS = 5     # Number of days to visualize (max 5 for free API)

# ---- FETCH WEATHER DATA ----
def fetch_weather(api_key, city):
    # OpenWeatherMap forecast endpoint (5 day / 3 hour forecast)
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data

def process_data(data):
    records = []
    for entry in data["list"]:
        dt = datetime.datetime.fromtimestamp(entry["dt"])
        temp = entry["main"]["temp"]
        humidity = entry["main"]["humidity"]
        records.append({
            "datetime": dt,
            "temperature": temp,
            "humidity": humidity
        })
    df = pd.DataFrame(records)
    return df

# ---- VISUALIZATION ----
def plot_weather(df, city):
    sns.set(style="whitegrid")
    df["datetime"] = pd.to_datetime(df["datetime"])

    # 🌡️ Temperature Trend
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df, x="datetime", y="temperature", marker="o", label="Temperature (°C)", color="tomato")
    plt.title(f"Temperature Forecast: {city}")
    plt.xlabel("Date & Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

    # 💧 Humidity Trend
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df, x="datetime", y="humidity", marker="o", label="Humidity (%)", color="deepskyblue")
    plt.title(f"Humidity Forecast: {city}")
    plt.xlabel("Date & Time")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    plt.show()

# ---- MAIN ----
if __name__ == "__main__":
    try:
        weather_data = fetch_weather(API_KEY, CITY)
        df = process_data(weather_data)
        plot_weather(df, CITY)
    except Exception as e:
        print("Error:", e)
        print("Make sure your API key is correct and the city name is valid.")