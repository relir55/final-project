import telebot
import requests

BOT_TOKEN = "8445866797:AAE6iqrJqyPuTixGEqc9avv89lKVUe09ftA"
API_KEY = "4dc9d5363b1cddd23f77a97a5a616385"

bot = telebot.TeleBot(BOT_TOKEN)

weather_icons = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧",
    "Drizzle": "🌦",
    "Thunderstorm": "⛈",
    "Snow": "❄️",
    "Mist": "🌫",
    "Fog": "🌫"
}

@bot.message_handler(commands=['start', 'hello'])
def start(message):
    bot.reply_to(message, "Привет! Я твой Тюменский, погодный бот! Напиши /weather чтобы посмотреть погоду в Тюмени на сегодня")

@bot.message_handler(commands=['weather'])
def weather(message):
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Tyumen&appid={API_KEY}&units=metric&lang=ru"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        bot.reply_to(message, f"Ошибка API: {data.get('message')}")
        return

    temp = data["main"]["temp"]
    feels = data["main"]["feels_like"]
    desc = data["weather"][0]["description"].capitalize()
    wind = data["wind"]["speed"]
    humidity = data["main"]["humidity"]
    main = data["weather"][0]["main"]

    # Количество осадков
    rain = data.get("rain", {}).get("1h", 0)
    snow = data.get("snow", {}).get("1h", 0)
    precipitation = rain + snow

    # Оценка влажности
    if humidity < 40:
        humidity_state = "Сухой воздух"
    elif humidity > 60:
        humidity_state = "Влажный воздух"
    else:
        humidity_state = "Комфортная влажность"

    # Рекомендации
    travel = "👍 Подходит для прогулок и путешествий" if wind < 10 and precipitation == 0 else "⚠️ Погода не лучшая для поездок"
    sport = "💪 Можно заниматься спортом" if wind < 7 and precipitation == 0 else "🚫 Спорт лучше отложить"

    icon = weather_icons.get(main, "🌍")

    bot.reply_to(message,
        f"{icon} Погода в Тюмени:\n"
        f"Температура: {temp}°C (ощущается как {feels}°C)\n"
        f"{desc}\n"
        f"💨 Ветер: {wind} м/с\n"
        f"💧 Влажность: {humidity}% — {humidity_state}\n"
        f"☔️ Осадки: {precipitation} мм/ч\n\n"
        f"🏖 {travel}\n"
        f"🤸 {sport}\n\n"
    )

bot.polling(none_stop=True)

