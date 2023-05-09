from aiogram import Bot, Dispatcher, executor,types
import requests

TOKEN_API = "*******"# put you token t_bot

bot = Bot(TOKEN_API)
dp = Dispatcher(bot)

@dp.message_handler()
async def daily(message: types.Message):

    #Get weather in yandexApi
    weater = requests.get("https://api.weather.yandex.ru/v2/informers?lat=&lon=", headers={'X-Yandex-API-Key':'***********'})# put api-key and lat lon yandex weather
    weater_json = weater.json() 
    dict_temp = weater_json['fact']['temp']

    #get feels temp
    feels_like = weater_json['fact']['feels_like']

    #get other factor (wind speed, wind_gust, pressure_mm)
    wind_speed = weater_json['fact']['wind_speed']
    wind_gust = weater_json['fact']['wind_gust']
    pressure_mm = weater_json['fact']['pressure_mm']

    #get conditions
    fact_condition = weater_json['fact']['condition']
    if fact_condition == 'clear':
        fact_condition = 'Ясно'
    elif fact_condition == 'partly-cloudy':
        fact_condition = 'Малооблачно'
    elif fact_condition == 'cloudy':
        fact_condition = 'Облачно с прояснениями'
    elif fact_condition == 'overcast':
        fact_condition = 'Пасмурно'
    elif fact_condition == 'drizzle':
        fact_condition = 'Морось'
    elif fact_condition == 'light-rain':
        fact_condition = 'Небольшой дождь'
    elif fact_condition == 'rain':
       fact_condition = 'Дождь'
    elif fact_condition == 'moderate-rain':
        fact_condition = 'Умеренно сильный дождь'
    elif fact_condition == 'heavy-rain':
        fact_condition = 'Сильный дождь'
    elif fact_condition == 'continuous-heavy-rain':
        fact_condition = 'Длительный сильный дождь'
    elif fact_condition == 'showers':
        fact_condition = 'Ливень'
    elif fact_condition == 'wet-snow':
        fact_condition = 'Дождь со снегом'
    elif fact_condition == 'light-snow':
        fact_condition = 'Небольшой снег'
    elif fact_condition == 'snow':
        fact_condition = 'Снег'
    elif fact_condition == 'snow-showers':
        fact_condition = 'Снегопад'
    elif fact_condition == 'hail':
        fact_condition = 'Град'
    elif fact_condition == 'thunderstorm':
        fact_condition = 'Гроза'
    elif fact_condition == 'thunderstorm-with-rain':
        fact_condition = 'Дождь с грозой'
    elif fact_condition == 'thunderstorm-with-hail':
        fact_condition = 'Гроза с градом'
    else:
        fact_condition = 'Апокалипсис'

    #Get rates in currate.ru
    cursrate = requests.get("https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=***********") #put apikey currqate.ru
    rates =cursrate.json()
    USDRUB = rates['data']['USDRUB']
    EURRUB = rates['data']['EURRUB']
    
    await message.answer(text = f'City {dict_temp}\u2103 Ощущается {feels_like}\u2103\n{fact_condition}\nВетер {wind_speed}м/с порывы до {wind_gust}м/с\nДавление {pressure_mm} мм\nКурс $ {USDRUB}\nКурс € {EURRUB}')


if __name__ == '__main__':
    executor.start_polling(dp)
