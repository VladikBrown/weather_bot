import logging
import requests
import json
import datetime
from emoji import emojize

from typing import Optional, Union, List, Dict
from dataclasses import dataclass

WEATHER_API_TOKEN = '8c3d69146bfed96cb6ba617467bd00c5'
KELVIN_CONST = +273.15
GET_CURRENT_WEATHER_BY_CITY_URL = 'http://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'
GET_5_DAY_FORECAST_BY_CITY_URL = 'https://api.openweathermap.org/data/2.5/forecast?q={0}&appid={1}'

weekdays_dict = {
    0: 'Mon',
    1: 'Tue',
    2: 'Wed',
    3: 'Thu',
    4: 'Fri',
    5: 'Sut',
    6: 'Sun'
}

MORNING_TIME = '09:00'
MIDDAY_TIME = '15:00'
EVENING_TIME = '21:00'
CELSIUS_SIGN = "°C"


@dataclass
class WeatherData:
    city: str
    current_temp: str
    feels_like: str
    weather: str
    weather_description: str
    date: str
    pretty_date: str
    time: str
    wind_speed: str


def get_5_day_forecast_by_city(city: str) -> Union[list, None]:
    weather_response = requests.get(GET_5_DAY_FORECAST_BY_CITY_URL.format(city, WEATHER_API_TOKEN))
    weather_data = json.loads(weather_response.text)
    weather_list = weather_data['list']
    city = weather_data['city']['name']
    if weather_data['cod'].__eq__('200'):
        return extract_5_week_weather_data(weather_list, city)
    else:
        return None


def get_today_forecast_by_city(city: str) -> Union[dict, None]:
    weather_response = requests.get(GET_5_DAY_FORECAST_BY_CITY_URL.format(city, WEATHER_API_TOKEN))
    weather_data = json.loads(weather_response.text)
    weather_list = weather_data['list']
    city = weather_data['city']['name']
    if weather_data['cod'].__eq__('200'):
        return __extract_certain_day_weather_data__(weather_list, city, 0)
    else:
        return None


def get_tomorrow_forecast_by_city(city: str) -> Union[dict, None]:
    weather_response = requests.get(GET_5_DAY_FORECAST_BY_CITY_URL.format(city, WEATHER_API_TOKEN))
    weather_data = json.loads(weather_response.text)
    weather_list = weather_data['list']
    city = weather_data['city']['name']
    if weather_data['cod'].__eq__('200'):
        return __extract_certain_day_weather_data__(weather_list, city, 1)
    else:
        return None


def extract_5_week_weather_data(weather_data: list, city) -> list:
    today_weather_data = list()
    for entry in weather_data:
        raw_date = entry['dt_txt']
        time = __get_time_from_date_raw__(raw_date)
        if time == MIDDAY_TIME:
            today_weather_data.append(__map_to_weather__(entry, city))
    return today_weather_data


def __extract_certain_day_weather_data__(weather_data: list, city: str, skip_days_number: int) -> dict:
    today_weather_data = dict()
    counter = int(0)
    for entry in weather_data:
        raw_date = entry['dt_txt']
        time = __get_time_from_date_raw__(raw_date)
        if time == "00:00":
            counter += 1
        if counter == skip_days_number:
            if time == MORNING_TIME:
                today_weather_data[MORNING_TIME] = __map_to_weather__(entry, city)
            elif time == MIDDAY_TIME:
                today_weather_data[MIDDAY_TIME] = __map_to_weather__(entry, city)
            elif time == EVENING_TIME:
                today_weather_data[EVENING_TIME] = __map_to_weather__(entry, city)
                return today_weather_data


def __map_to_weather__(weather_map: dict, city) -> WeatherData:
    current_temp = str(kelvin_celsius_temp(weather_map['main']['temp'])) + CELSIUS_SIGN
    feels_like = str(kelvin_celsius_temp(weather_map['main']['feels_like'])) + CELSIUS_SIGN
    weather = weather_map['weather'][0]['main']
    weather_description = weather_map['weather'][0]['description'].capitalize()
    raw_date = weather_map['dt_txt']
    pretty_date = __parse_date_to_pretty__(raw_date)
    time = __get_time_from_date_raw__(raw_date)
    wind_speed = "{0} m/s".format(round(weather_map['wind']['speed']))
    return WeatherData(current_temp=current_temp, feels_like=feels_like, weather=weather, city=city,
                       weather_description=weather_description, date=raw_date, pretty_date=pretty_date,
                       time=time, wind_speed=wind_speed)


def __parse_date_to_pretty__(date_raw: str):
    date = date_raw.split(" ")[0]
    date_parts = date.split("-")
    day = date_parts[2]
    months = date_parts[1]
    year = date_parts[0]
    day_of_week = weekdays_dict[datetime.datetime(int(year), int(months), int(day)).weekday()]
    return "{0}.{1} ({2})".format(day, months, day_of_week)


def __get_date_of_week_from_raw_date__(date_raw: str):
    date_parts = date_raw.split(" ")[0].split("-")
    return weekdays_dict[datetime.datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2])).weekday()]


def __get_time_from_date_raw__(date_raw: str):
    time_raw = date_raw.split(" ")[1].split(":")
    time_pretty = time_raw[0] + ":" + time_raw[1]
    return time_pretty


def kelvin_celsius_temp(temp: float):
    return format_float_temp(temp - KELVIN_CONST)


def format_float_temp(temp: float):
    return float("{0:.1f}".format(temp)).__str__()


if __name__ == '__main__':
    x = get_today_forecast_by_city("Minsk")
    print(x)
