import requests
import config


class Weather:
    def __init__(self):
        """ Initialization """
        self.url = 'https://api.openweathermap.org/data/2.5/'
        self.token = config.tokens['weather']
        self.r = requests

    def get_city(self, name):
        """ Gets id of city """
        request = self.url + f'weather?q={name}&units=metric&appid={self.token}'
        data = self.r.get(request).json()

        if data['cod'] == 200:
            city = {'name': data['name'], 'id': data['id']}
            return city

        return None

    def get_current(self, name):
        """ Gets current weather """
        city = self.get_city(name)

        if not city == None: 
            city_id = city['id']
            request = self.url + f'weather?id={city_id}&units=metric&appid={self.token}'
            data = self.r.get(request).json()

            current_weather = {'name': data['name'],
                               'temp': data['main']['temp'],
                               'wind': data['wind']['speed'],
                               'humidity': data['main']['humidity'],
                               'id': data['weather'][0]['id']}

            return current_weather

        return None