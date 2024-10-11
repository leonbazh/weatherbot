import requests

API_KEY = 'your_api_key'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=en"
    response = requests.get(url)
    # checking status code
    if response.status_code != 200:
        raise ValueError("City was not found.")
    
    data = response.json()

    weather = {
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed']
    }
    return weather
