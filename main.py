import telebot
import requests
import weather
from weather_db import log_request, create_table

# Init bot
API_TOKEN = 'bot_api_key'
bot = telebot.TeleBot(API_TOKEN)

# /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello! This bot was created for a test task in BobrAI. Type /weather <city> to find out the weather ")

# /weather
@bot.message_handler(commands=['weather'])
def get_weather(message):
    try:
        # Getting the city from the user's message

        city = message.text.replace('/weather', '').strip()        
        if not city:
            raise ValueError('Сity is not specified or is incorrect. Please use: /weather <city>')
        
        # Getting weather data
        weather_data = weather.get_weather(city)
        response = correct_response(city,weather_data)

        # Sending message to user
        bot.send_message(message.chat.id, response)

        # Logging request in db
        log_request(message.chat.id, message.text, response) 

    except ValueError as err:
        response = str(err)
        bot.send_message(message.chat.id, response)
        log_request(message.chat.id, message.text, response) # Remove line to create logs without error


    except Exception as err:
        response = "Weather api error, mayber lost connection, try again later"
        bot.send_message(message.chat.id, response)
        log_request(message.chat.id, message.text, response) # Remove line to create logs without error

        

def correct_response(city, weather_data):
    return f"Weather in {city}:\n" \
           f"Temp: {weather_data['temp']}°C\n" \
           f"Feels like: {weather_data['feels_like']}°C\n" \
           f"Description: {weather_data['description']}\n" \
           f"Humidity: {weather_data['humidity']}%\n" \
           f"Wind speed: {weather_data['wind_speed']} m/s"

# Starting bot and creating table in PostgreSQL
if __name__ == '__main__':
    create_table()
    bot.polling(none_stop=True)
