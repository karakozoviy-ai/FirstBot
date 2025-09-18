from BotTel.My_imp import  *

API_KEY_WEATHER = "4aac91a8f6224f62890155659252008"  # Ваш ключ WeatherAPI
LOCATION_LAT = 53.200
LOCATION_LON = 50.150
DAYS = 2  # Количество дней прогноза


router = Router()
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


def data_formatted(weather_date):
    date_string = weather_date['current']['last_updated']
    # Преобразуем строку в объект datetime
    datetime_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M')  # Укажите правильный формат!
    # Форматируем объект datetime в нужный формат
    formatted_date = datetime_object.strftime('%d.%m.%Y %H:%M')
    return formatted_date


def weather_to_day(weather: set()):
    weather_date = data_formatted(weather)
    weath_now = {"temp": weather['current']['temp_c'], "date_now": weather_date,
                 "ico": weather['current']['condition']['icon']}
    return weath_now
def get_hourly_temperature(data):
    hourly_temperatures = {}
    for hour_data in data['hour']:
        time = hour_data['time']
        temperature = hour_data['temp_c']  # Или 'temp_f', если вам нужна температура в Фаренгейтах
        hourly_temperatures[time] = temperature
    return hourly_temperatures
get_weather_to_day = get_weather_day(LOCATION_LAT, LOCATION_LON)
w_today = weather_to_day(get_weather_to_day)



#pprint(get_weather_forecast(LOCATION_LAT,LOCATION_LON,DAYS))
# Этот хэндлер будет срабатывать на команду "/weather_now"
@router.message(Command(commands='weather_now'))
async def process_calories_command(message: Message):
    ico_filename = w_today["ico"]
    await message.answer_photo(
        photo=f'https:{ico_filename}',  # Или await bot.send_photo, если bot не доступен через message
        caption=f"Время: {w_today['date_now']}, Температура: {w_today['temp']}"
    )
