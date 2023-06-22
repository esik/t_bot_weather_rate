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
    cursrate = requests.get("https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=***********") #put apikey currqate.ru
    rates =cursrate.json()
    USDRUB = rates['data']['USDRUB']
    EURRUB = rates['data']['EURRUB']
    
    await message.answer(text = f'City {dict_temp}\u2103 Ощущается {feels_like}\u2103\n{fact_condition}\nВетер {wind_speed}м/с порывы до {wind_gust}м/с\nДавление {pressure_mm} мм\nКурс $ {USDRUB}\nКурс € {EURRUB}')


if __name__ == '__main__':
    executor.start_polling(dp)
