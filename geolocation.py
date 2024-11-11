from telegram import Update
from telegram.ext import ContextTypes
from weather_by_location import get_weather_by_location


# Функция для обработки геолокации пользователя
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    location = update.message.location
    if location:
        lat, lon = location.latitude, location.longitude
        weather_info = get_weather_by_location(lat, lon)
        await update.message.reply_text(weather_info)
