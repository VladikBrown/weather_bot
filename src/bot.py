import logging
import emoji

from service.weather_service import *
from aiogram import Bot, Dispatcher, executor, types

TG_API_TOKEN = '2012534020:AAG2_QJjtCbHrdm3FJvM7pOvT47MfPF_mao'
KELVIN_CONST = +273.15

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TG_API_TOKEN)
dp = Dispatcher(bot)
weather_service = WeatherService()

emoji = {'Cloud': emoji.emojize(":cloud:"), 'Clear': emoji.emojize(':sun:')}


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm YourWeatherBot!\n Please enter your city.")


@dp.message_handler()
async def get_weather_handler(city: types.Message):
    # check if city exist
    weather = weather_service.get_current_weather_by_city(city.text)

    await city.answer(format_message(weather))


def format_message(weather: Weather):
    if weather is not None:
        return "Current temperature in Minsk\n" + "Actual: " \
           + format_float_temp(weather.current_temp) + "\nFeels like: " + format_float_temp(weather.feels_like)
    else:
        return "We don't know such city yet. Please check if you spell it correctly or try another one"


def format_float_temp(temp: float):
    return float("{0:.1f}".format(temp)).__str__()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
