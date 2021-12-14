import logging
import requests
import json

from typing import Optional, Union
from dataclasses import dataclass

WEATHER_API_TOKEN = '8c3d69146bfed96cb6ba617467bd00c5'
KELVIN_CONST = +273.15
GET_WEATHER_BY_CITY_URL = 'http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'


@dataclass
class WeatherData:
    city: str
    current_temp: float
    feels_like: float
    weather: str
    weather_description: str
    date: str
    pretty_date: str
    time: str


#todo
def get_5_day_forecast() -> list[WeatherData]:
    pass


def get_current_weather_by_city(city: str) -> Union[WeatherData, None]:
    weather_response = requests.get(GET_WEATHER_BY_CITY_URL.format(city, WEATHER_API_TOKEN))
    weather_dict = json.loads(weather_response.text)
    if weather_dict['cod'].__eq__('200'):
        return __map_to_weather__(weather_dict)
    else:
        return None


def __map_to_weather__(weather_map: dict) -> WeatherData:
    current_temp = kelvin_celsius_temp(weather_map['main']['temp'])
    feels_like = kelvin_celsius_temp(weather_map['main']['feels_like'])
    weather = weather_map['weather'][0]['main']
    weather_description = weather_map['weather'][0]['description']
    date = weather_map['dt_txt']
    pretty_date = __parse_date_to_pretty__(date)
    city = weather_map['name']
    return WeatherData(current_temp=current_temp, feels_like=feels_like, weather=weather, city=city)


#todo
def __parse_date_to_pretty__(date_raw: str):
    #todo 2021-12-15 03:00:00
    date = date_raw.split(" ")[0]
    time = date_raw.split(" ")[1]
    date_parts = date.split("-")
    day = date_parts[2]
    months = date_parts[1]
    pass


def kelvin_celsius_temp(temp: float):
    return temp - KELVIN_CONST


def format_float_temp(temp: float):
    return float("{0:.1f}".format(temp)).__str__()
