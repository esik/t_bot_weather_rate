import asyncio
from aiogram import Bot, Dispatcher, executor,types
import requests

from config import TOKEN_TBOT_API,RATE_API_KEY,YANDEX_API_KEY,CORDINATE
import schedule
import time


bot = Bot(TOKEN_TBOT_API)
dp = Dispatcher(bot)

async def send_message():

    #Get weather in yandexApi
    weater = requests.get(f"https://api.weather.yandex.ru/v2/informers?{CORDINATE}", headers={'X-Yandex-API-Key':f'{YANDEX_API_KEY}'})# put api-key and lat lon yandex weather
    weater_json = weater.json() 
    print(weater_json)
    dict_temp = weater_json['fact']['temp']

    #get feels temp
    feels_like = weater_json['fact']['feels_like']

    #get other factor (wind speed, wind_gust, pressure_mm)
    wind_speed = weater_json['fact']['wind_speed']
    wind_gust = weater_json['fact']['wind_gust']
    pressure_mm = weater_json['fact']['pressure_mm']

    #get conditions
    conditions = {
    'clear': 'Ясно',
    'partly-cloudy': 'Малооблачно',
    'cloudy': 'Облачно с прояснениями',
    'overcast': 'Пасмурно',
    'drizzle': 'Морось',
    'light-rain': 'Небольшой дождь',
    'rain': 'Дождь',
    'moderate-rain': 'Умеренно сильный дождь',
    'heavy-rain': 'Сильный дождь',
    'continuous-heavy-rain': 'Длительный сильный дождь',
    'showers': 'Ливень',
    'wet-snow': 'Дождь со снегом',
    'light-snow': 'Небольшой снег',
    'snow': 'Снег',
    'snow-showers': 'Снегопад',
    'hail': 'Град',
    'thunderstorm': 'Гроза',
    'thunderstorm-with-rain': 'Дождь с грозой',
    'thunderstorm-with-hail': 'Гроза с градом'
}
    fact_condition = weater_json['fact']['condition']
    fact_condition = conditions.get(fact_condition, 'Апокалипсис')
    
    #Get rates in currate.ru
    cursrate = requests.get(f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={RATE_API_KEY}") #put apikey currqate.ru
    rates =cursrate.json()
    USDRUB = rates['data']['USDRUB']
    EURRUB = rates['data']['EURRUB']
    
    await bot.send_message(chat_id='438467198',text = f'City {dict_temp}\u2103 Ощущается {feels_like}\u2103\n{fact_condition}\nВетер {wind_speed}м/с порывы до {wind_gust}м/с\nДавление {pressure_mm} мм\nКурс $ {USDRUB}\nКурс € {EURRUB}')

@dp.message_handler()
async def daily(message: types.Message):
    await send_message()


def schedule_task():
    schedule.every().day.at("08:00").do(asyncio.run, send_message())  # Устанавливаем время отправки сообщения

    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == '__main__':
    schedule_task()
    executor.start_polling(dp)
# from aiogram import Bot, Dispatcher, executor,types
# import requests

# from config import TOKEN_TBOT_API,RATE_API_KEY,YANDEX_API_KEY,CORDINATE



# bot = Bot(TOKEN_TBOT_API)
# dp = Dispatcher(bot)

# @dp.message_handler()
# async def daily(message: types.Message):

#     #Get weather in yandexApi
#     weater = requests.get(f"https://api.weather.yandex.ru/v2/informers?{CORDINATE}", headers={'X-Yandex-API-Key':f'{YANDEX_API_KEY}'})# put api-key and lat lon yandex weather
#     weater_json = weater.json() 
#     print(weater_json)
#     dict_temp = weater_json['fact']['temp']

#     #get feels temp
#     feels_like = weater_json['fact']['feels_like']

#     #get other factor (wind speed, wind_gust, pressure_mm)
#     wind_speed = weater_json['fact']['wind_speed']
#     wind_gust = weater_json['fact']['wind_gust']
#     pressure_mm = weater_json['fact']['pressure_mm']

#     #get conditions
#     conditions = {
#     'clear': 'Ясно',
#     'partly-cloudy': 'Малооблачно',
#     'cloudy': 'Облачно с прояснениями',
#     'overcast': 'Пасмурно',
#     'drizzle': 'Морось',
#     'light-rain': 'Небольшой дождь',
#     'rain': 'Дождь',
#     'moderate-rain': 'Умеренно сильный дождь',
#     'heavy-rain': 'Сильный дождь',
#     'continuous-heavy-rain': 'Длительный сильный дождь',
#     'showers': 'Ливень',
#     'wet-snow': 'Дождь со снегом',
#     'light-snow': 'Небольшой снег',
#     'snow': 'Снег',
#     'snow-showers': 'Снегопад',
#     'hail': 'Град',
#     'thunderstorm': 'Гроза',
#     'thunderstorm-with-rain': 'Дождь с грозой',
#     'thunderstorm-with-hail': 'Гроза с градом'
# }
#     fact_condition = weater_json['fact']['condition']
#     fact_condition = conditions.get(fact_condition, 'Апокалипсис')
    
#     #Get rates in currate.ru
#     cursrate = requests.get(f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={RATE_API_KEY}") #put apikey currqate.ru
#     rates =cursrate.json()
#     USDRUB = rates['data']['USDRUB']
#     EURRUB = rates['data']['EURRUB']
    
#     await message.answer(text = f'City {dict_temp}\u2103 Ощущается {feels_like}\u2103\n{fact_condition}\nВетер {wind_speed}м/с порывы до {wind_gust}м/с\nДавление {pressure_mm} мм\nКурс $ {USDRUB}\nКурс € {EURRUB}')


# if __name__ == '__main__':
#     executor.start_polling(dp)


# from aiogram import Bot, Dispatcher, executor, types
# import aiohttp

# from config import TOKEN_TBOT_API, RATE_API_KEY, YANDEX_API_KEY

# YANDEX_WEATHER_API_URL = "https://api.weather.yandex.ru/v2/informers?lat=&lon="
# CURRENCY_RATES_API_URL = f"https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key={RATE_API_KEY}"

# CITY_CONDITIONS = {
#     'clear': 'Ясно',
#     'partly-cloudy': 'Малооблачно',
#     'cloudy': 'Облачно с прояснениями',
#     'overcast': 'Пасмурно',
#     'drizzle': 'Морось',
#     'light-rain': 'Небольшой дождь',
#     'rain': 'Дождь',
#     'moderate-rain': 'Умеренно сильный дождь',
#     'heavy-rain': 'Сильный дождь',
#     'continuous-heavy-rain': 'Длительный сильный дождь',
#     'showers': 'Ливень',
#     'wet-snow': 'Дождь со снегом',
#     'light-snow': 'Небольшой снег',
#     'snow': 'Снег',
#     'snow-showers': 'Снегопад',
#     'hail': 'Град',
#     'thunderstorm': 'Гроза',
#     'thunderstorm-with-rain': 'Дождь с грозой',
#     'thunderstorm-with-hail': 'Гроза с градом'
# }

# bot = Bot(TOKEN_TBOT_API)
# dp = Dispatcher(bot)


# @dp.message_handler()
# async def daily(message: types.Message):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(YANDEX_WEATHER_API_URL, headers={'X-Yandex-API-Key': YANDEX_API_KEY}) as weather_response:
#             weather_data = await weather_response.json()

#         async with session.get(CURRENCY_RATES_API_URL) as currency_response:
#             currency_data = await currency_response.json()

#     dict_temp = weather_data['fact']['temp']
#     feels_like = weather_data['fact']['feels_like']
#     wind_speed = weather_data['fact']['wind_speed']
#     wind_gust = weather_data['fact']['wind_gust']
#     pressure_mm = weather_data['fact']['pressure_mm
