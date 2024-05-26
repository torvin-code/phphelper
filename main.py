import os
import datetime
import time
import pytz
import calendar
import requests
import weatherapi
import rssnewsparser
from dotenv import load_dotenv

load_dotenv()

WEATHERAPI_TOKEN = os.getenv('WEATHERAPI_TOKEN')
WEATHERAPI_GEO = os.getenv('WEATHERAPI_GEO')
TELEGRAM_BOT_TOKEN =  os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID =  os.getenv('TELEGRAM_CHAT_ID')
USER_LOCAL_TIMEZONE =  os.getenv('USER_LOCAL_TIMEZONE')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')
JSON_API_KEY = os.getenv('JSON_API_KEY')
JSON_BIN = os.getenv('JSON_BIN')

days_of_week = {
    "Monday": "Понедельник",
    "Tuesday": "Вторник",
    "Wednesday": "Среда",
    "Thursday": "Четверг",
    "Friday": "Пятница",
    "Saturday": "Суббота",
    "Sunday": "Воскресенье"
}

months = {
    "January": "Января",
    "February": "Февраля",
    "March": "Марта",
    "April": "Апреля",
    "May": "Мая",
    "June": "Июня",
    "July": "Июля",
    "August": "Августа",
    "September": "Сентября",
    "October": "Октября",
    "November": "Ноября",
    "December": "Декабря"
}


def current_time():
    user_tz = pytz.timezone(USER_LOCAL_TIMEZONE)
    now = datetime.datetime.now(user_tz)
    hours = now.hour
    return int(hours)


def current_day():
    user_tz = pytz.timezone(USER_LOCAL_TIMEZONE)
    now = datetime.datetime.now(user_tz)
    day = now.day
    number_month = now.month
    month = months[calendar.month_name[number_month]]
    year = now.year
    day_of_week = calendar.weekday(year, number_month, day)
    full_day_name = days_of_week[calendar.day_name[day_of_week]]  
    return f"Сегодня {day} {month}, {full_day_name}"


def rss():
    data = rssnewsparser.get_new_posts(JSON_API_KEY, JSON_BIN)
    if len(data) > 0:
        for post in data:
            tg_send_post(post)
            time.sleep(5)


def tg_send_message(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
    }
    response = requests.post(url, json=data)
    resp = response.json()
    #print(resp)


def tg_send_post(text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url, json=data)
    resp = response.json()
    print(resp)




def main():
    c_time = current_time()
    if c_time == 6:
        message = current_day()
        weather = weatherapi.weatherapi_current(WEATHERAPI_TOKEN, WEATHERAPI_GEO)
        if weather is not None:
            if weather != '':
                message += "\n\n" + weather
        tg_send_message(message)
        time.sleep(5)      
        weather_forecastday = weatherapi.weatherapi_forecastday(WEATHERAPI_TOKEN, WEATHERAPI_GEO)
        if weather_forecastday is not None:
            if weather_forecastday != '':
                tg_send_message(weather_forecastday)
    else:
        weather = weatherapi.weatherapi_current(WEATHERAPI_TOKEN, WEATHERAPI_GEO)
        if weather is not None:
            if weather != '':
                tg_send_message(weather)
    rss()


if __name__ == "__main__":
    main()
