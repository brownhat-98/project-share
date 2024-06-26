
import requests

def get_weather_data(city):
    api_key = '4b6dc24f12bce1a90dd4bf9768b0edf3'
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'description': data['weather'][0]['description'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'icon': data['weather'][0]['icon'],
        }
        return weather
    else:
        return None
