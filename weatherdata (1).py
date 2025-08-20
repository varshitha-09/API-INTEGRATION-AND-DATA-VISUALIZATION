import requests
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

# 🔐 Paste your OpenWeatherMap API key here 
API_KEY = 'cc9290d74149d1c92333a5a353c0a34c'
API_URL = 'https://api.openweathermap.org/data/2.5/forecast'

def fetch_weather_data(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        print("❌ Failed to fetch weather data. Check your city name or API key.")
        return None

    data = response.json()
    timestamps, temps, humidities, winds, summaries = [], [], [], [], defaultdict(list)

    for entry in data["list"]:
        dt = datetime.strptime(entry["dt_txt"], "%Y-%m-%d %H:%M:%S")
        timestamps.append(dt)
        temps.append(entry["main"]["temp"])
        humidities.append(entry["main"]["humidity"])
        winds.append(entry["wind"]["speed"])
        date_only = dt.date()
        summaries[date_only].append({
            "temp": entry["main"]["temp"],
            "condition": entry["weather"][0]["main"]
        })

    return timestamps, temps, humidities, winds, summaries

def plot_line_chart(x, y, ylabel, title, color):
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker='o', color=color)
    plt.title(title)
    plt.xlabel("Date & Time")
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def display_summary(summary_data):
    print("\n--- 🧾 Daily Forecast Summary ---")
    for date, entries in summary_data.items():
        temps = [e["temp"] for e in entries]
        conditions = [e["condition"] for e in entries]
        most_common = max(set(conditions), key=conditions.count)
        print(f"{date.strftime('%A, %b %d')}: 🌡️ High {max(temps):.1f}°C | Low {min(temps):.1f}°C | 🌥️ Condition: {most_common}")

def main():
    city = input("Enter city name: ")
    data = fetch_weather_data(city)
    if data:
        timestamps, temps, humidities, winds, summary = data

        print("\n📈 Plotting weather trends...")
        plot_line_chart(timestamps, temps, "Temperature (°C)", f"Temperature Trend for {city}", "orange")
        plot_line_chart(timestamps, humidities, "Humidity (%)", f"Humidity Trend for {city}", "blue")
        plot_line_chart(timestamps, winds, "Wind Speed (m/s)", f"Wind Speed Trend for {city}", "green")

        display_summary(summary)

if __name__ == "__main__":
    main()
