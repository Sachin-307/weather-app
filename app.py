from flask import Flask, render_template, request
import requests
import os




app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = os.getenv("WEATHER_API_KEY")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city")
    if not city:
        return render_template("index.html", error="Please enter a city name.")
    
    url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        # Extracting data based on the JSON structure you provided
        weather_data = {
            "city": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "feels_like": data["current"]["feelslike_c"],
            "description": data["current"]["condition"]["text"],
            "icon": data["current"]["condition"]["icon"],
            "humidity": data["current"]["humidity"],
            "wind_speed": data["current"]["wind_kph"],
            "pressure": data["current"]["pressure_mb"]
        }
        return render_template("result.html", weather=weather_data)
    else:
        # Improved error handling for API errors
        error_message = response.json().get("error", {}).get("message", "An error occurred.")
        return render_template("index.html", error=f"Error: {error_message}")


if __name__ == "__main__":
    app.run(debug=True)
