# from aiogram.types import ReplyKeyboardRemove, \
#  ReplyKeyboardMarkup, \
#   InlineKeyboardMarkup, InlineKeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.constants import *

# button_menu_weather = InlineKeyboardButton('Weather', callback_data='menu_weather')
# button_menu_notifications = InlineKeyboardButton('Notifications', callback_data='menu_notifications')

# keyboard_menu = InlineKeyboardMarkup(resize_keyboard=True).add(button_menu_weather, button_menu_notifications)

main_menu_keyboard = [[
    InlineKeyboardButton(WEATHER_BUTTON_LABEL, callback_data=WEATHER_BUTTON_CALLBACK_DATA),
    InlineKeyboardButton(NOTIFICATION_BUTTON_LABEL, callback_data=NOTIFICATION_BUTTON_CALLBACK_DATA),
]]
main_menu_reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

set_up_notification_keyboard = [
    [
        InlineKeyboardButton(NOTIFICATION_MORNING_LABEL, callback_data=NOTIFICATION_MORNING_CALLBACK_DATA)
    ],
    [
        InlineKeyboardButton(NOTIFICATION_EVENING_LABEL, callback_data=NOTIFICATION_EVENING_CALLBACK_DATA)
    ],
    [
        InlineKeyboardButton(NOTIFICATION_DISABLE_LABEL, callback_data=DISABLE_NOTIFICATION_CALLBACK_DATA)
    ]
]

set_up_notification_reply_markup = InlineKeyboardMarkup(set_up_notification_keyboard)

select_forecast_keyboard = [
    [
        InlineKeyboardButton(TODAY_FORECAST_LABEL, callback_data=TODAY_FORECAST_CALLBACK_DATA)
    ],
    [
        InlineKeyboardButton(WEEK_FORECAST_LABEL, callback_data=WEEK_FORECAST_CALLBACK_DATA)
    ]
]

select_forecast_reply_markup = InlineKeyboardMarkup(select_forecast_keyboard)
