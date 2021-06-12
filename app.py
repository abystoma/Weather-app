from flask import Flask, render_template, request, flash, redirect

from flask_sqlalchemy import SQLAlchemy
import requests
import time
import sys
import os
api_key=os.environ.get('WEATHER_API_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'loren_ipsum'

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return self.name
db.create_all()

def find_background(time: int) -> str:
    if 7 < time < 17:
        return 'day'
    elif 20 > time <= 23 or 0 < time < 6:
        return 'night'
    else:
        return 'evening-morning'
    
def find_weather(city: str, city_id: int):
    data = None
    api_site = "http://api.openweathermap.org/data/2.5/weather"
    queries = {'q': city, 'units': 'metric','appid': api_key}
    r = requests.get(api_site,params=queries)       
    if r:
        result = r.json()
        gmt_time = time.gmtime().tm_hour
        local_time =  time.gmtime().tm_hour + int(result['timezone']) // 3600
        background_image = find_background(local_time)
        data = {'city': result['name'], 
                'temp': result['main']['temp'], 
                'timezone': background_image,
                'weather': result['weather'][0]['main'],
                'id': city_id,
                'country':result['sys']['country']
                }
    return data


@app.route('/', methods=['GET'])
def index(): 
    cities = City.query.all()
    cities_weather = []
    for city in cities:
        cities_weather.append(find_weather(city, city.id))
        
    return render_template('index.html', data = cities_weather)


@app.route('/add',methods = ['POST'])
def add():
    if request.method == 'POST':
        city_name = request.form.get('city_name')

        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather',params = {'q': city_name,'appid': api_key})

        if response.status_code == 404:
            flash("The city doesn't exist!")
            return redirect('/')

        cities = City.query.all()
        for city in cities:
            if city.name == city_name:
                flash("The city has already been added to the list!")
                return redirect('/')
        else:
            city = City(name=city_name)
            db.session.add(city)
            db.session.commit()
            return redirect('/')
        
@app.route('/delete/<city_id>', methods=['GET', 'POST'])
def delete(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')
# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
    
#url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=api_key"