import requests
import datetime
import sys
import Weather


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    # Функция для получения всех сообщений, отправленных боту.
    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, data=params)
        result_json = resp.json()['result']
        return result_json

    # Функция для отправки ответов пользователю.
    def send_mess(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, data=params)
        return resp

    # Функция для получения последнего сообщения,
    # отправленного боту.
    def last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update


# Функция для определения приветствия
# в зависимости от времени суток.
def get_greeting():
    now = datetime.datetime.now()
    hour = now.hour

    if 6 <= hour < 12:
        greeting = 'Доброе утро'
    elif 12 <= hour < 17:
        greeting = 'Добрый день'
    elif 17 <= hour < 23:
        greeting = 'Добрый вечер'

    return greeting


# Функция для вывода подсказки по использованию.
def show_help():
    print('Использование бота: python Weater_bot.py --token [your_token]')


# Функция для получения токена.
def get_token(list_of_args):
    if len(list_of_args) == 2 and list_of_args[0] == '--token':
        token = list_of_args[1]
    else:
        show_help()
        exit()
    return token


def main(token):
    greetings = ('здравствуй!', 'ку!', 'привет!', 'здорово!', 'привет',
                 'здравствуй', 'ку', 'здорово', 'салют', 'салют!')
    greet_bot = BotHandler(token)
    new_offset = None

    while True:
        greet_bot.get_updates(new_offset)
        last_update = greet_bot.last_update()

        # Если нет новых сообщений, ничего не делаем.
        if last_update is None:
            continue

        # Получаем данные о сообщении.
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']

        # Обрабатываем сообщение.
        if last_chat_text.lower() in greetings:
            greeting = get_greeting()
            greet_bot.send_mess(last_chat_id, '{}, {}!'.format(greeting, last_chat_name))
        elif last_chat_text.lower() == '/погода':
            weather_data = Weather.show_weather_spb()
            weather_string = '\n'.join(weather_data)
            greet_bot.send_mess(last_chat_id, weather_string)

        # Инкрементируем счетчик сообщений.
        new_offset = last_update_id + 1


if __name__ == '__main__':
    token = get_token(sys.argv[1:])
    try:
        main(token)
    except KeyboardInterrupt:
        exit()
