# Weather App

## About
A simple Flask app that works with database, handling post and get requests. 

## Features of the app
1. The app takes the name of the city as input and shows the current state of the weather and temperature.
2. Background image which which changes with time of the city.
3. The user will be able to delete the weather information.

## Installation and dependencies
1. The app uses the api from [OpenWeather](https://openweathermap.org/) to fetch the weather information. [Sign up](https://home.openweathermap.org/users/sign_up) here to get an API key for yourself.

2. Create a user environment variable with variable name `WEATHER_API_KEY` and put the API key in variable value ![img](https://i.imgur.com/YA7wfyu.png)

3. ```
   git clone https://github.com/flukehermit/Weather-app.git
   cd weather-app
   pip install -r requirements.txt
   ```
## Syntax for running the app
```
python app.py
```
## Example
<img src="https://i.imgur.com/DSVGSX1.gif"/>
