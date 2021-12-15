from src.service.weather_service import *

emoji_mapping = {
    'Thunderstorm': ':zap:',
    'Drizzle': ':umbrella:',
    'Rain': ':umbrella:',
    'Snow': ':snowflake:',
    'Clear': ':sunny:',
    'Clouds': ':cloud:'
}


def format_weekly_forecast(weather: list):
    result_message = str()
    for entry in weather:
        result_message += (format_week_weather_entry(entry))
    return result_message


def format_week_weather_entry(weather: WeatherData):
    return "{0} - {1} ({2}), {3}, {4}\n".format(weather.pretty_date, weather.current_temp, weather.wind_speed,
                                              weather.weather_description, emoji_mapping[weather.weather])


#rewrite this shit GOVNOOOOO
def format_daily_forecast(weather: dict) -> str:
    morning_weather = weather[MORNING_TIME]
    midday_weather = weather[MIDDAY_TIME]
    evening_weather = weather[EVENING_TIME]
    return MORNING_TIME + ": " + " {0} ({1}), {2}, {3} {4}\n" \
        .format(morning_weather.current_temp, morning_weather.feels_like, morning_weather.wind_speed,
                morning_weather.weather_description,
                emoji_mapping[morning_weather.weather]) + \
           MIDDAY_TIME + ": " + " {0} ({1}), {2}, {3} {4}\n" \
               .format(midday_weather.current_temp, midday_weather.feels_like, midday_weather.wind_speed,
                       midday_weather.weather_description,
                       emoji_mapping[midday_weather.weather]) + \
           EVENING_TIME + ": " + " {0} ({1}), {2}, {3} {4}\n" \
               .format(evening_weather.current_temp, evening_weather.feels_like, evening_weather.wind_speed,
                       evening_weather.weather_description,
                       emoji_mapping[evening_weather.weather])