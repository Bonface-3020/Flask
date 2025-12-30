from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY=os.getenv("Weather_Map_API")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/get_weather",methods=['POST'])
def get_weather():
    city=request.form.get("city")

    if not city or not validate_city_name(city):
        return render_template("index.html",error="Invalid city name")
    
    base_url="https://api.openweathermap.org/data/2.5/weather"
    params={
        "q":city,
        "appid":API_KEY,
        "units":"metric"
    }
    response=requests.get(base_url,params=params)

    if response.status_code==200:
        data=response.json()
        weather= {
            "city": data["name"],
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
        return render_template("index.html",weather=weather)
    elif response==404:
        return render_template("index.html",error="City not found")
    else:
        return render_template("index.html",error="unable to fetch weather, try again!")

def validate_city_name(city):
    return all(part.isalpha()  for part in city.split()) and len(city)>1

if __name__ == "__main__":
    app.run(debug=True)    
    
