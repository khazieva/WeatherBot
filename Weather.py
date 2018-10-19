import requests


def show_weather_spb():
    weather_data = []
    weather_url = 'https://www.metaweather.com/api/location'
    res = requests.get('{}/search/?query=St%20Petersburg'.format(weather_url))
    res = res.json()
    city_id = res[0]["woeid"]
    location = requests.get('{}/{}/'.format(weather_url, city_id))
    location = location.json()

    for weather in location["consolidated_weather"]:
        format_str = 'Дата {}, min t {:.1f}°C, max t {:.1f}°C'
        weather_str = format_str.format(weather["applicable_date"], weather["min_temp"], weather["max_temp"])
        weather_data.append(weather_str)

    return weather_data
