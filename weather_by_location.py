import requests

API_KEY = 'API key OpenWeather'


# функция получения погоды по API на данный момент по координатам
def get_weather_by_location(lat: float, lon: float) -> str:
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        city = data['name']
        return f"Погода в {city}:\n{weather.capitalize()}\nТемпература: {temp}°C\nВлажность: {humidity}%"
    else:
        return "Ошибка: не удалось получить данные о погоде для вашего местоположения."
