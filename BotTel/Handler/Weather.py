from BotTel.My_imp import *
from aiogram.types import BufferedInputFile
from aiogram import F
from BotTel.BotToken import API_KEY_W


API_KEY_WEATHER = API_KEY_W
LOCATION_LAT = 53.200
LOCATION_LON = 50.150
LOCATION_NAME = "Самара"

router = Router()


# Создаем клавиатуру с кнопками
def get_weather_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="🌞 Погода сегодня")
    builder.button(text="🌅 Погода завтра")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_weather_forecast(latitude, longitude, days):
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY_WEATHER}&q={latitude},{longitude}&lang=ru&days={days}&aqi=no&alerts=no"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к WeatherAPI: {e}")
        return None


def create_weather_table_image(forecast_data, city_name, day_offset=0):
    """Создает изображение с таблицей почасового прогноза погоды для указанного дня"""

    if day_offset >= len(forecast_data['forecast']['forecastday']):
        day_offset = 0  # Fallback to today if requested day doesn't exist

    forecast_day = forecast_data['forecast']['forecastday'][day_offset]
    location = forecast_data['location']['name']
    current_date = forecast_day['date']
    hours = forecast_day['hour']

    # Размеры и параметры таблицы
    table_width = 800
    row_height = 40
    icon_size = 40
    font_size = 16
    header_height = 80

    num_rows = len(hours)
    table_height = header_height + num_rows * row_height
    image = Image.new("RGB", (table_width, table_height), color="white")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Заголовок таблицы
    day_names = ["сегодня", "завтра", "послезавтра"]
    day_name = day_names[day_offset] if day_offset < len(day_names) else f"через {day_offset} дней"

    header_text = f"Погода в {location} на {current_date} ({day_name})"
    draw.text((table_width // 2, header_height // 4), header_text, font=font, fill="black", anchor="mm")

    # Заголовки столбцов
    col_headers = ["Иконка", "Время", "Температура (°C)"]
    col_widths = [100, 200, 200]

    # Координаты для заголовков столбцов
    y_headers = header_height - row_height

    x = 0
    for i, header in enumerate(col_headers):
        draw.text((x + col_widths[i] // 2, y_headers + row_height // 2),
                  header, font=font, fill="black", anchor="mm")
        x += col_widths[i]

    # Линия под заголовками
    draw.line((0, header_height, table_width, header_height), fill="black", width=2)

    # Данные таблицы
    y = header_height

    for hour_data in hours:
        time = datetime.fromisoformat(hour_data['time']).strftime('%H:%M')
        temperature = hour_data['temp_c']
        icon_url = "https:" + hour_data['condition']['icon']
        x = 0

        # Загрузка иконки
        try:
            icon_response = requests.get(icon_url, stream=True)
            icon_response.raise_for_status()
            icon_file = io.BytesIO(icon_response.content)
            icon = Image.open(icon_file)
            icon = icon.resize((icon_size, icon_size))
            image.paste(icon, (x + col_widths[0] // 2 - icon_size // 2,
                               y + row_height // 2 - icon_size // 2), icon)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке иконки: {e}")

        # Время
        draw.text((col_widths[0] + col_widths[1] // 2, y + row_height // 2),
                  time, font=font, fill="black", anchor="mm")

        # Температура
        temperature_text = f'{temperature}°C'
        draw.text((col_widths[0] + col_widths[1] + col_widths[2] // 2, y + row_height // 2),
                  temperature_text, font=font, fill="black", anchor="mm")

        # Вертикальные линии
        for i, width in enumerate(col_widths[:-1]):
            x_line = sum(col_widths[:i + 1])
            draw.line((x_line, y, x_line, y + row_height), fill='black')

        # Горизонтальная линия
        draw.line((0, y + row_height, table_width, y + row_height), fill="black")
        y += row_height

    # Внешняя рамка таблицы
    draw.rectangle([0, header_height - row_height, table_width, table_height],
                   outline="black", width=2)

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


@router.message(Command(commands=['weather_now', 'погода']))
async def process_weather_command(message: Message):
    """Обработчик команды /weather - показывает клавиатуру"""
    keyboard = get_weather_keyboard()
    await message.answer("Выберите период прогноза погоды:", reply_markup=keyboard)


@router.message(F.text == "🌞 Погода сегодня")
async def process_weather_today(message: Message):
    """Обработчик кнопки 'Погода сегодня'"""
    forecast_data = get_weather_forecast(LOCATION_LAT, LOCATION_LON, 2)  # Получаем 2 дня для страховки
    if forecast_data:
        photo_table = create_weather_table_image(forecast_data, LOCATION_NAME, 0)
        photo_table = BufferedInputFile(photo_table, filename="weather_today.png")
        await message.answer_photo(photo=photo_table, caption="🌞 Погода на сегодня")
    else:
        await message.answer("❌ Не удалось получить данные о погоде")


@router.message(F.text == "🌅 Погода завтра")
async def process_weather_tomorrow(message: Message):
    """Обработчик кнопки 'Погода завтра'"""
    forecast_data = get_weather_forecast(LOCATION_LAT, LOCATION_LON, 2)
    if forecast_data and len(forecast_data['forecast']['forecastday']) > 1:
        photo_table = create_weather_table_image(forecast_data, LOCATION_NAME, 1)
        photo_table = BufferedInputFile(photo_table, filename="weather_tomorrow.png")
        await message.answer_photo(photo=photo_table, caption="🌅 Погода на завтра")
    else:
        await message.answer("❌ Не удалось получить прогноз на завтра")




