from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from city import ask_city, back, handle_city_input, ask_city_menu, handle_weather_choice
from geolocation import handle_location


TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'


# Главная функция при входе в бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    btn_name_city = KeyboardButton("Указать город")
    btn_geolocation_city = KeyboardButton("Геолокация", request_location=True)
    keyboard = [[btn_name_city, btn_geolocation_city]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет! Я помогу тебе с прогнозом погоды. Выбери, что хочешь сделать:",
                                    reply_markup=reply_markup)


def main():
    # Используем Application вместо Updater
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Регистрация обработчика команды /weather
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Text("Указать город"), ask_city_menu))
    application.add_handler(MessageHandler(filters.Text("Назад"), back))
    application.add_handler(MessageHandler(filters.Text("Погода сейчас"), handle_weather_choice))
    application.add_handler(MessageHandler(filters.Text("Погода на 1 день"), handle_weather_choice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_input))
    application.add_handler(MessageHandler(filters.LOCATION, handle_location))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()
