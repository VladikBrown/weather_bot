import logging
import requests
import json

from dataclasses import dataclass

WEATHER_API_TOKEN = '8c3d69146bfed96cb6ba617467bd00c5'
KELVIN_CONST = +273.15
GET_WEATHER_BY_CITY_URL = 'http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'


@dataclass
class Weather:
    current_temp: float
    feels_like: float
    weather: str


class WeatherService:
    def get_current_weather_by_city(self, city: str):
        weather_response = requests.get(GET_WEATHER_BY_CITY_URL.format(city, WEATHER_API_TOKEN))
        weather_dict = json.loads(weather_response.text)
        if weather_dict['cod'].__eq__('200'):
            return self.__map_to_weather__(weather_dict)
        else:
            return None

    def __map_to_weather__(self, weather_map: dict):
        current_temp = self.kelvin_celsius_temp(weather_map['main']['temp'])
        feels_like = self.kelvin_celsius_temp(weather_map['main']['feels_like'])
        weather = weather_map['weather'][0]['main']
        return Weather(current_temp=current_temp, feels_like=feels_like, weather=weather)

    def kelvin_celsius_temp(self, temp: float):
        return temp - KELVIN_CONST


def format_float_temp(temp: float):
    return float("{0:.1f}".format(temp)).__str__()
