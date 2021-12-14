import logging
import emoji
import bot.keyboards as kb
from service.weather_service import *
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.utils import BotStates
from bot.config import TG_API_TOKEN
import aioschedule
import asyncio
from datetime import datetime
import aiocron

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, InlineKeyboardButton

KELVIN_CONST = +273.15

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
bot = Bot(token=TG_API_TOKEN, loop=loop)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
weather_service = WeatherService()

emoji = {'Cloud': emoji.emojize(":cloud:"), 'Clear': emoji.emojize(':sun:')}


@dp.callback_query_handler(lambda c: c.data == 'menu_weather')
async def process_callback_weather(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(BotStates.STATE_1)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Please enter your city!')


@dp.callback_query_handler(lambda c: c.data == 'menu_notifications')
async def process_callback_weather(callback_query: types.CallbackQuery):
    state = dp.current_state(user=callback_query.from_user.id)
    await state.set_state(BotStates.STATE_2)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Notification!')
    loops = asyncio.get_event_loop()
    loops.call_later(3, repeat, loops)


async def send_message(chat_id):
    await bot.send_message(chat_id=chat_id, text="Hello!")


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(3, repeat, coro, loop)


async def cron_message(chat_id):
        await asyncio.sleep(5)
        await send_message(chat_id)
        await asyncio.create_task(cron_message(chat_id))


@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_ids = message.chat.id
    await state.reset_state()
    await message.reply("Hi!\nI'm YourWeatherBot!\n", reply_markup=kb.keyboard_menu)


@dp.message_handler(state=BotStates.STATE_1)
async def get_weather_handler(city: types.Message):
    # check if city exist
    weather = weather_service.get_current_weather_by_city(city.text)
    await city.answer(format_message(weather))


def format_message(weather: WeatherData):
    if weather is not None:
        return "Current temperature in Minsk\n" + "Actual: " \
               + format_float_temp(weather.current_temp) + "\nFeels like: " + format_float_temp(weather.feels_like)
    else:
        return "We don't know such city yet. Please check if you spell it correctly or try another one"


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
