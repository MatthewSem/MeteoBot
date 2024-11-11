import requests

API_KEY = 'API key OpenWeather'


# функция получения погоды по API на данный момент по городу
def get_weather(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        return f"Погода в {city.capitalize()}:\n{weather.capitalize()}\nТемпература: {temp}°C\nВлажность: {humidity}%"
    else:
        return "Ошибка: не удалось получить данные о погоде. Проверьте название города."


# Функция получения погоды на 1 день с интервалом в 3 часа
def get_weather_1day_6hour(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast = f"Прогноз погоды для города {city.capitalize()}:\n"

        # Массив с метками для утра, дня и вечера
        time_labels = ['Утро', 'День', 'Вечер']
        time_hours = [6, 12, 18]  # Часы для утро, день, вечер

        # Перебираем прогнозы, выбираем только для 6, 12 и 18 часов
        count = 0
        for entry in data['list']:
            dt = entry['dt_txt']
            hour = int(dt.split()[1].split(':')[0])  # Извлекаем час из временной метки

            if hour in time_hours and count < 3:
                weather = entry['weather'][0]['description']  # Описание погоды
                temp = entry['main']['temp']  # Температура
                humidity = entry['main']['humidity']  # Влажность

                # Добавляем прогноз с соответствующей меткой (Утро, День, Вечер)
                forecast += f"\n---{time_labels[count]}---\n{weather.capitalize()},\nТемпература: {temp}°C,\nВлажность: {humidity}%\n\n"

                count += 1

            if count >= 3:
                break  # Прерываем цикл, если получили 3 прогноза

        return forecast
    else:
        return "Ошибка: не удалось получить данные о прогнозе погоды. Проверьте название города."


def get_weather_3_days(city: str) -> str:
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        forecast = ""
        count = 0
        # Прогноз на 3 дня: отбираем первые 3 дня (первый день — это первая запись в прогнозе)
        for item in data['list'][:24]:  # 24 записи = 1 день с 3-часовыми интервалами
            if count == 8:  # Примерно через 8 записей можно брать каждый день
                date = item['dt_txt']
                temp = item['main']['temp']
                weather = item['weather'][0]['description']
                forecast += f"Дата: {date}\nТемпература: {temp}°C\nПогода: {weather.capitalize()}\n\n"
                count = 0
            count += 1
        return forecast
    else:
        return "Ошибка: не удалось получить данные о прогнозе на 3 дня."