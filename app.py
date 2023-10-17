from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

# Replace 'your_api_key_here' with your actual OpenWeatherMap API key
api_key = "beb18a2f7bd96eed827053f5518f2eb3"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        city = request.form['city']
        country = request.form['country']

        # Make the 5-day forecast API request
        weather_url = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?q={city},{country}&appid={api_key}&units=metric'
        )

        weather_data = weather_url.json()

        # Extract and display the forecast for the next 5 days
        forecast = []

        for entry in weather_data['list']:
            timestamp = entry['dt']  # Timestamp for the forecast entry
            temperature = entry['main']['temp']  # Temperature
            weather_description = entry['weather'][0]['description']  # Weather condition

            # Format the timestamp as a readable date and time
            formatted_timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

            forecast.append({
                'timestamp': formatted_timestamp,
                'temperature': temperature,
                'weather_description': weather_description
            })

        return render_template("forecast.html", forecast=forecast, city=city)

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
