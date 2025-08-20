from turtledemo.clock import current_day

import requests
from pprint import pprint
from datetime import datetime, timedelta

API_KEY_WEATHER = "4aac91a8f6224f62890155659252008"  # Ваш ключ WeatherAPI
LOCATION_LAT = 53.200
LOCATION_LON = 50.150
DAYS = 2  # Количество дней прогноза
def get_weather_day(latitude, longitude):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY_WEATHER}&q={latitude},{longitude}&lang=ru&aqi=no&alerts=no"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к WeatherAPI: {e}")
        return None
def get_weather_forecast(latitude, longitude, days):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY_WEATHER}&q={latitude},{longitude}&lang=ru&days={days}&aqi=no&alerts=no"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к WeatherAPI: {e}")
        return None

def weather_to_day(weather : set()):
    date_string = get_weather_to_day['current']['last_updated']
    # Преобразуем строку в объект datetime
    datetime_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M')  # Укажите правильный формат!
    # Форматируем объект datetime в нужный формат
    formatted_date = datetime_object.strftime('%d.%m.%Y %H:%M')
    return f"На {formatted_date} в г. Самара температура = {get_weather_to_day['current']['temp_c']}"
get_weather_to_day = get_weather_forecast(LOCATION_LAT,LOCATION_LON,DAYS)
w_today = weather_to_day(get_weather_to_day)
#pprint(get_weather_forecast(LOCATION_LAT,LOCATION_LON,DAYS))
