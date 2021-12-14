from telegram.ext import MessageFilter


class WeatherFilter(MessageFilter):
    def filter(self, message):
        return {'attribute_name': ['weather']}


class NotificationFilter(MessageFilter):
    def filter(self, message):
        return {'attribute_name': ['notification']}
