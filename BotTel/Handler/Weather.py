from BotTel.My_imp import  *
from aiogram.types import BufferedInputFile
API_KEY_WEATHER = "4aac91a8f6224f62890155659252008"  # Ваш ключ WeatherAPI
LOCATION_LAT = 53.200
LOCATION_LON = 50.150
LOCATION_NAME = "Самара"
DAYS = 1  # Количество дней прогноза


router = Router()

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


def create_weather_table_image(forecast_data, city_name):
    """Создает изображение с таблицей почасового прогноза погоды."""

    location = forecast_data['location']['name']
    current_date = forecast_data['forecast']['forecastday'][0]['date']
    hours = forecast_data['forecast']['forecastday'][0]['hour']

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
    header_text = f"Погода в {location} на {current_date}"
    draw.text((table_width // 2, header_height // 4), header_text, font=font, fill="black", anchor="mm")

    # Заголовки столбцов - РИСУЕМ В ОТДЕЛЬНОЙ СЕКЦИИ
    col_headers = ["Иконка", "Время", "Температура (°C)"]
    col_widths = [100, 200, 200]

    # Координаты для заголовков столбцов
    y_headers = header_height - row_height  # Заголовки выше данных

    x = 0
    for i, header in enumerate(col_headers):
        draw.text((x + col_widths[i] // 2, y_headers + row_height // 2),
                  header, font=font, fill="black", anchor="mm")
        x += col_widths[i]

    # Линия под заголовками
    draw.line((0, header_height, table_width, header_height), fill="black", width=2)

    # Данные таблицы (начинаем после заголовков)
    y = header_height  # Начинаем с header_height, а не header_height

    for hour_data in hours:
        time = datetime.fromisoformat(hour_data['time']).strftime('%H:%M')
        temperature = hour_data['temp_c']
        icon_url = "https:" + hour_data['condition']['icon']
        x = 0  # Сбрасываем x в начало для каждой строки

        # Загрузка иконки
        try:
            icon_response = requests.get(icon_url, stream=True)
            icon_response.raise_for_status()
            icon_file = io.BytesIO(icon_response.content)
            icon = Image.open(icon_file)
            icon = icon.resize((icon_size, icon_size))
            # Позиционируем иконку в первом столбце
            image.paste(icon, (x + col_widths[0] // 2 - icon_size // 2,
                               y + row_height // 2 - icon_size // 2), icon)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке иконки: {e}")

        # Время (второй столбец)
        draw.text((col_widths[0] + col_widths[1] // 2, y + row_height // 2),
                  time, font=font, fill="black", anchor="mm")

        # Температура (третий столбец)
        temperature_text = f'{temperature}°C'
        draw.text((col_widths[0] + col_widths[1] + col_widths[2] // 2, y + row_height // 2),
                  temperature_text, font=font, fill="black", anchor="mm")

        # Вертикальные линии между столбцами
        for i, width in enumerate(col_widths[:-1]):
            x_line = sum(col_widths[:i + 1])
            draw.line((x_line, y, x_line, y + row_height), fill='black')

        # Горизонтальная линия под строкой
        draw.line((0, y + row_height, table_width, y + row_height), fill="black")

        y += row_height

    # Внешняя рамка таблицы
    draw.rectangle([0, header_height - row_height, table_width, table_height],
                   outline="black", width=2)

    # Сохраняем изображение в байты
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr
@router.message(Command(commands='weather_now'))
async def process_weather_command(message: Message):
    forecast_data = get_weather_forecast(LOCATION_LAT, LOCATION_LON, DAYS)
    photo_table = create_weather_table_image(forecast_data, LOCATION_NAME)
    photo_table = BufferedInputFile(photo_table, filename="weather_table.png")
    await message.answer_photo(photo=photo_table, caption="Погода на день")
