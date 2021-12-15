from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from bot.config import TG_API_TOKEN
from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler, MessageFilter, ConversationHandler
from telegram.ext import CallbackContext
import logging
from telegram.ext import CommandHandler

from service.weather_service import *
from bot.filters import WeatherFilter, NotificationFilter
from bot.constants import *

from bot.keyboards import main_menu_reply_markup, set_up_notification_reply_markup, select_forecast_keyboard, \
    select_forecast_reply_markup
from src.bot.message_formatter import format_daily_forecast, format_weekly_forecast

updater = Updater(token=TG_API_TOKEN, use_context=True)
jq = updater.job_queue
dispatcher = updater.dispatcher
MENU, WEATHER, NOTIFICATION, INPUT_WEATHER = range(4)
notification_jobs = list()

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi!\nI'm YourWeatherBot!\n",
                             reply_markup=main_menu_reply_markup)
    return MENU


# match data:
# case 'weather':
# handle_weather_button(update, context)
# return WEATHER
# case 'notification':
# handle_weather_button(update, context)
# return NOTIFICATION
# case 'morning':
# set_up_notification(update, context, when='morning')
# return MENU
# case 'evening':
# set_up_notification(update, context, when='evening')
# return MENU
# case 'disable_notifications':
# disable_notifications(update, context)
def button_pressed_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    query.answer()

    if data == 'weather':
        handle_weather_button(update, context)
        return WEATHER
    elif data == 'notification':
        handle_weather_button(update, context)
        return NOTIFICATION
    elif data == 'morning':
        set_up_notification(update, context, when='morning')
        return MENU
    elif data == 'evening':
        set_up_notification(update, context, when='evening')
        return MENU
    elif data == 'disable_notifications':
        disable_notifications(update, context)
        return MENU
    elif data == 'today':
        get_forecast(update, context)
        return MENU
    elif data == 'week':
        get_forecast(update, context)
        return MENU


def handle_weather_button(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Please enter your city!')
    if data == 'weather':
        return WEATHER
    elif data == 'notification':
        return NOTIFICATION


def get_forecast(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    reply = str()
    city = context.user_data['city']
    if data == TODAY_FORECAST_CALLBACK_DATA:
        weather = get_today_forecast_by_city(city)
        if weather is not None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emojize(format_daily_forecast(weather)),
                                     reply_markup=main_menu_reply_markup)
        #todo we don't know such city
    elif data == WEEK_FORECAST_CALLBACK_DATA:
        weather = get_5_day_forecast_by_city(city)
        if weather is not None:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=emojize(format_weekly_forecast(weather)),
                                     reply_markup=main_menu_reply_markup)
    return MENU


def handle_notification_button(update: Update, context: CallbackContext):
    query = update.callback_query
    print(query.data)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Please enter your city!')
    return NOTIFICATION


def get_weather(update: Update, context: CallbackContext):
    weather = get_today_forecast_by_city(update.message.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text=format_daily_forecast_message(weather))


def get_weather_by_city(context: CallbackContext):
    job_context = context.job.context
    weather = get_today_forecast_by_city(job_context['city'])
    context.bot.send_message(chat_id=job_context['chat_id'], text=format_daily_forecast_message(weather))


def set_up_notification(update: Update, context: CallbackContext, when: str):
    global job_minute
    city = context.user_data['city']
    weather = get_today_forecast_by_city(city)
    job_context = {'chat_id': update.effective_chat.id, 'city': city}
    if weather is not None:
        if when == 'morning':
            job_minute = jq.run_repeating(get_weather_by_city, context=job_context, interval=10, first=10)
        elif when == 'evening':
            job_minute = jq.run_repeating(get_weather_by_city, context=job_context, interval=5, first=5)

        notification_jobs.append(job_minute)
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Notification for each {0} is successfully set".format(when),
                                 reply_markup=main_menu_reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="We don't know such city yet. "
                                      "Please check if you spell it correctly or try another one",
                                 reply_markup=main_menu_reply_markup)

    return MENU


def disable_notifications(update, context):
    drop_all_notifications()
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="All {0} notifications disabled".format(str(notification_jobs.__sizeof__())),
                             reply_markup=main_menu_reply_markup)
    return MENU


def drop_all_notifications():
    for job in notification_jobs:
        job.schedule_removal()
    logging.info("All {0} notifications disabled".format(str(notification_jobs.__sizeof__())))


def set_city_for_notification(update: Update, context: CallbackContext):
    key = 'city'
    value = update.message.text
    context.user_data[key] = value
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='Please select when do you want to get forecast',
                             reply_markup=set_up_notification_reply_markup)
    return MENU


def set_city_for_weather(update: Update, context: CallbackContext):
    key = 'city'
    value = update.message.text
    context.user_data[key] = value
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text='What forecast?',
                             reply_markup=select_forecast_reply_markup)
    return MENU


def format_daily_forecast_message(weather: WeatherData):
    if weather is not None:
        return "Current weather in {0}\n Actual: {1} \n Feels like: {2}\n " \
            .format(weather.city,
                    weather.current_temp,
                    weather.feels_like)
    else:
        return "We don't know such city yet. Please check if you spell it correctly or try another one"


def main():
    start_handler = CommandHandler('start', start)

    weather_filter = WeatherFilter()
    notification_filter = NotificationFilter()

    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [CallbackQueryHandler(button_pressed_handler)],
            WEATHER: [MessageHandler(Filters.text & ~Filters.command, set_city_for_weather)],
            NOTIFICATION: [MessageHandler(Filters.text & ~Filters.command, set_city_for_notification)]
        },
        fallbacks=[CommandHandler('cancel', start)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
