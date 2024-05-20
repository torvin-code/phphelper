import requests

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'

moon_phase_dict = {
    "New Moon": "Новолуние",
    "Waxing Crescent": "Первая четверть",
    "First Quarter": "Первая четверть",
    "Waxing Gibbous": "Вторая четверть",
    "Full Moon": "Полнолуние",
    "Waning Gibbous ": "Третья четверть",
    "Last Quarter": "Последняя четверть",
	"Waning Crescent": "Последняя четверть",
}


def weatherapi_current(WEATHERAPI_TOKEN, WEATHERAPI_GEO):
    resp_text = temp_c = text_weather = wind_kph = ''
    wind_dir = gust_kph = pressure_mb = precip_mm = ''
    humidity = cloud = uv = ''
    headers = {'user-agent': USER_AGENT}
    url = f"https://api.weatherapi.com/v1/current.json?key={WEATHERAPI_TOKEN}&q={WEATHERAPI_GEO}&aqi=no&lang=ru"
    r = requests.get(url, headers=headers)
    a = r.status_code
    if a == 200:
        resp = r.json()
        if 'current' in resp.keys():
            if 'temp_c' in resp['current'].keys():
                temp_c = str(int(round(resp['current']['temp_c'])))
            if 'condition' in resp['current'].keys():
                if 'text' in resp['current']['condition'].keys():
                    text_weather = resp['current']['condition']['text'].strip()
                    if text_weather != '':
                        text_weather = ', '+ text_weather
            resp_text += f"Температура {temp_c}°{text_weather}"+"\n"

            if 'wind_kph' in resp['current'].keys():
                wind_kph = resp['current']['wind_kph']
            if 'wind_dir' in resp['current'].keys():
                wind_dir = resp['current']['wind_dir'].strip()
            if  str(wind_kph).strip() != '':
                wind_kph = wind_kph * 0.27778
                wind_kph = str(int(round(wind_kph)))
                wind_kph = f"Скорость ветра {wind_kph} м/с" 
                if wind_dir != '':
                    wind_kph += f", {wind_dir}"
            if wind_kph != '':
                resp_text += wind_kph+"\n"

            if 'gust_kph' in resp['current'].keys():
                gust_kph = resp['current']['gust_kph']
            if str(gust_kph).strip() != '':
                gust_kph = gust_kph * 0.27778
                gust_kph = str(int(round(gust_kph)))
                resp_text += f"Порывы ветра до {gust_kph} м/с"+"\n"

            if 'pressure_mb' in resp['current'].keys():
                pressure_mb = resp['current']['pressure_mb']
            if pressure_mb != '':
                pressure_mb = pressure_mb * 0.75006375541921
                pressure_mb = str(int(round(pressure_mb)))
                resp_text += f"Давление: {pressure_mb} мм.рт.ст."+"\n" 

            if 'precip_mm' in resp['current'].keys():
                precip_mm = str(resp['current']['precip_mm']).strip()
            if precip_mm != '':
                resp_text += f"Количество осадков: {precip_mm} мм."+"\n" 

            if 'humidity' in resp['current'].keys():
                humidity = str(resp['current']['humidity']).strip()
            if humidity != '':
                resp_text += f"Влажность: {humidity}%"+"\n" 

            if 'cloud' in resp['current'].keys():
                cloud = str(resp['current']['cloud']).strip()
            if cloud != '':
                resp_text += f"Облачность: {cloud}%"+"\n"  

            if 'uv' in resp['current'].keys():
                uv = str(resp['current']['uv']).strip()
            if uv != '':
                resp_text += f"УФ-индекс: {uv}"+"\n"                  
        return resp_text 




def weatherapi_forecastday(WEATHERAPI_TOKEN, WEATHERAPI_GEO):
    resp_text = forecastday = astro = whour = ''
    headers = {'user-agent': USER_AGENT}
    url = f"https://api.weatherapi.com/v1/forecast.json?key={WEATHERAPI_TOKEN}&q={WEATHERAPI_GEO}&days=1&aqi=no&alerts=no&lang=ru"
    r = requests.get(url, headers=headers)
    a = r.status_code
    if a == 200:
        resp = r.json()
        if 'forecast' in resp.keys():
            if 'forecastday' in resp['forecast'].keys():
                if 'date' in resp['forecast']['forecastday'][0].keys():
                    resp_text += resp['forecast']['forecastday'][0]['date']+"\n\n"
                if 'day' in resp['forecast']['forecastday'][0].keys():
                    forecastday = resp['forecast']['forecastday'][0]['day']
                    forecastday = weatherapi_day(forecastday)
                    resp_text += forecastday+"\n"
                if 'astro' in resp['forecast']['forecastday'][0].keys():
                    astro = resp['forecast']['forecastday'][0]['astro']
                    astro = weatherapi_astro(astro)
                    resp_text += astro+"\n"
                if 'hour' in resp['forecast']['forecastday'][0].keys():
                    whour = resp['forecast']['forecastday'][0]['hour']
                    whour = weatherapi_hours(whour)
                    resp_text += whour+"\n"
    return resp_text


def weatherapi_day(forecastday):
    resp_text = avgtemp_c = maxtemp_c = mintemp_c = ''
    text_weather = maxwind_kph = daily_chance_of_rain = ''
    avghumidity = totalprecip_mm = uv = ''
    if 'avgtemp_c' in forecastday.keys():
        avgtemp_c = str(int(round(forecastday['avgtemp_c']))).strip()
    if 'maxtemp_c' in forecastday.keys():
        maxtemp_c = str(int(round(forecastday['maxtemp_c']))).strip()
    if 'mintemp_c' in forecastday.keys():
        mintemp_c = str(int(round(forecastday['mintemp_c']))).strip()
    if 'condition' in forecastday.keys():
        if 'text' in forecastday['condition'].keys():
            text_weather = forecastday['condition']['text'].strip()
            if text_weather != '':
                text_weather = ', '+ text_weather
    resp_text += f"Температура {avgtemp_c}°C ({mintemp_c}°- {maxtemp_c}°){text_weather}"+"\n"
    if 'maxwind_kph' in forecastday.keys():
        maxwind_kph = forecastday['maxwind_kph']
    if  str(maxwind_kph).strip() != '':
        maxwind_kph = maxwind_kph * 0.27778
        maxwind_kph = str(int(round(maxwind_kph)))
        resp_text += f"Скорость ветра: {maxwind_kph} м/с"+"\n"
    if 'daily_chance_of_rain' in forecastday.keys():
        daily_chance_of_rain = str(forecastday['daily_chance_of_rain'])
        resp_text += f"Вероятность дождя: {daily_chance_of_rain}%"+"\n"
    if 'avghumidity' in forecastday.keys():
        avghumidity = str(forecastday['avghumidity'])
        resp_text += f"Средняя влажность: {avghumidity}%"+"\n"
    if 'totalprecip_mm' in forecastday.keys():
        totalprecip_mm = str(int(round(forecastday['totalprecip_mm'])))
        resp_text += f"Количество осадков: {totalprecip_mm}мм."+"\n"
    if 'uv' in forecastday.keys():
        uv = str(forecastday['uv']).strip()
    if uv != '':
        resp_text += f"УФ-индекс: {uv}"+"\n"  
    return resp_text


def weatherapi_astro(astro):
    resp_text = sunrise = sunset = ''
    moonrise = moonset = moon_phase = ''
    moon_illumination = ''
    if 'sunrise' in astro.keys():
        sunrise = astro['sunrise'].strip()
    if 'sunset' in astro.keys():
        sunset = astro['sunset'].strip()
    if 'moonrise' in astro.keys():
        moonrise = astro['moonrise'].strip()
    if 'moonset' in astro.keys():
        moonset = astro['moonset'].strip()
    if 'moon_phase' in astro.keys():
        moon_phase = astro['moon_phase'].strip()
        if moon_phase in moon_phase_dict.keys():
            moon_phase = moon_phase_dict[moon_phase]
    if 'moon_illumination' in astro.keys():
        moon_illumination = str(int(round(astro['moon_illumination'])))
    resp_text += f"Восход Солнца: {sunrise}"+"\n"
    resp_text += f"Заход Солнца: {sunset}"+"\n"
    resp_text += f"Восход Луны: {moonrise}"+"\n"
    resp_text += f"Заход Луны: {moonset}"+"\n"
    resp_text += f"Фаза Луны: {moon_phase}"+"\n"
    resp_text += f"Яркость Луны: {moon_illumination}%"+"\n"
    return resp_text


def weatherapi_hours(whours):
    resp_text = temp_c = text_weather = ''
    wind_dir = wind_kph = ''
    whours_dict = []  
    for whour in whours:
        item = ''
        if 'time' in whour.keys():
            wtime = whour['time'].split()[1]
        if 'temp_c' in whour.keys():
            temp_c = str(int(round(whour['temp_c'])))
        if 'condition' in whour.keys():
            if 'text' in whour['condition'].keys():
                text_weather = whour['condition']['text'].strip()
                if text_weather != '':
                    text_weather = ', '+ text_weather
        item += f"{wtime}  {temp_c}°C{text_weather}"

        if 'wind_kph' in whour.keys():
            wind_kph = whour['wind_kph']
        if 'wind_dir' in whour.keys():
            wind_dir = whour['wind_dir'].strip()
        if  str(wind_kph).strip() != '':
            wind_kph = wind_kph * 0.27778
            wind_kph = str(int(round(wind_kph)))
            wind_kph = f", {wind_kph} м/с" 
            if wind_dir != '':
                wind_kph += f", {wind_dir}"
        if wind_kph != '':
            item += wind_kph
        whours_dict.append(item)
    if len(whours_dict) > 0:
        resp_text = "\n".join(whours_dict)
    return resp_text

