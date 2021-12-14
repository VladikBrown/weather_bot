# from aiogram.types import ReplyKeyboardRemove, \
#  ReplyKeyboardMarkup, \
#   InlineKeyboardMarkup, InlineKeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src.bot.constants import WEATHER_BUTTON_LABEL, NOTIFICATION_BUTTON_LABEL, WEATHER_BUTTON_CALLBACK_DATA, \
    NOTIFICATION_BUTTON_CALLBACK_DATA, NOTIFICATION_MORNING_LABEL, NOTIFICATION_EVENING_LABEL, \
    NOTIFICATION_MORNING_CALLBACK_DATA, NOTIFICATION_EVENING_CALLBACK_DATA, NOTIFICATION_DISABLE_LABEL, \
    DISABLE_NOTIFICATION_CALLBACK_DATA

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