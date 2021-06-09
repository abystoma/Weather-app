from flask import Flask
from flask import render_template
from flask import request
import requests
import time
import sys
import os

api_key = os.environ.get('WEATHER_API_KEY')
app = Flask(__name__)

def find_background(time: int) -> str:
    if 7 < time < 17:
        return 'day'
    elif 20 > time <= 23 or 0 < time < 6:
        return 'night'
    else:
        return 'evening-morning'
    
def find_weather(city: str) -> dict:
    data = None
    api_site = "http://api.openweathermap.org/data/2.5/weather"
    queries = {'q': city, 'units': 'metric','appid': api_key}
    r = requests.get(api_site,params=queries)       
    if r:
        result = r.json()
        gmt_time = time.gmtime().tm_hour
        local_time =  time.gmtime().tm_hour + int(result['timezone']) // 3600
        background_image = find_background(local_time)
        data = {'city': result['name'], 'temp': result['main']['temp'], 'timezone': background_image,
                'weather': result['weather'][0]['main']}
    return data

default_weather = [find_weather('tokyo'), find_weather('alaska'), find_weather('new york')]
cities_weather = []

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        city_name = request.form['city_name']
        city = find_weather(city_name)
        if city:
            cities_weather.append(city)
        return render_template('index.html', data = default_weather + cities_weather)
    else:
        return render_template('index.html', data=default_weather)


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
    
#url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=api_key"