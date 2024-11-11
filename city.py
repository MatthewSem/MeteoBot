from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from weather_by_city import get_weather, get_weather_1day_6hour


# Функция при нажатии кнопки Указать город
async def ask_city_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    btn_on_now_day = KeyboardButton("Погода сейчас")
    btn_on_one_day = KeyboardButton("Погода на 1 день")
    btn_back = KeyboardButton("Назад")
    back_keyboard = [[btn_on_now_day, btn_on_one_day],
                     [btn_back]]
    reply_markup = ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)
    context.user_data['current_menu'] = 'ask_city_menu'
    await update.message.reply_text("Пожалуйста, выберите за какой период вас интересует прогноз.",
                                    reply_markup=reply_markup)

# Функция при нажатии кнопки Погода сейчас или Погода на 1 день
async def handle_weather_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "Погода сейчас":
        context.user_data['current_variable'] = 'Погода сейчас'  # Устанавливаем меню для текущей погоды
        await ask_city(update, context)
    elif update.message.text == "Погода на 1 день":
        context.user_data['current_variable'] = 'Погода на 1 день'  # Устанавливаем меню для прогноза на 1 день
        await ask_city(update, context)

async def ask_city(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    btn_back = KeyboardButton("Назад")
    back_keyboard = [[btn_back]]
    reply_markup = ReplyKeyboardMarkup(back_keyboard, resize_keyboard=True)
    context.user_data['awaiting_city'] = True
    context.user_data['current_menu'] = 'ask_city'
    await update.message.reply_text("Пожалуйста, введите название города, чтобы получить прогноз погоды.", reply_markup=reply_markup)


# Функция при нажатии кнопки Назад
async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    curren_menu = context.user_data.get('current_menu', 'start')
    if curren_menu == 'ask_city_menu':
        btn_name_city = KeyboardButton("Указать город")
        btn_geolocation_city = KeyboardButton("Геолокация", request_location=True)
        keyboard = [[btn_name_city, btn_geolocation_city]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "Вы вернулись в главное меню. Выберите действие:",
            reply_markup=reply_markup
        )
    elif curren_menu == 'ask_city':
        await ask_city_menu(update, context)


# Функция для обработки ввода города и отправки прогноза
async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('awaiting_city'):
        city = update.message.text
        if context.user_data.get('current_variable') == 'Погода на 1 день':
            weather_info = get_weather_1day_6hour(city)
        else:
            weather_info = get_weather(city)

        await update.message.reply_text(weather_info)
        context.user_data['awaiting_city'] = False
        await back(update, context)
