import requests
import config
from io import BytesIO


class Bot:
    def __init__(self):
        """ Initialization """
        self.token = config.tokens['bot']
        self.url = 'https://api.telegram.org/bot' + self.token + '/'
        self.r = requests
        self.last_update = None
        self.last_id = None

    def get_html(self, url):
        """ Gets html from webpage """
        data = self.r.get(url).json()
        return data

    def get_updates(self):
        """ Gets updates from telegram """
        request = self.url + f'getUpdates?offset={self.last_id}'
        data = self.get_html(request)
        self.last_id = data['result'][-1]['update_id']
        return data

    def get_message(self):
        """ Gets last message """
        data = self.get_updates()

        if not self.last_update == data['result'][-1]['update_id']:

            chat_id = data['result'][-1]['message']['chat']['id']
            text = data['result'][-1]['message']['text']
            self.last_update = data['result'][-1]['update_id']
            log = {'text': str(text),
                   'user': data['result'][-1]['message']['from']['first_name'],
                   'id': data['result'][-1]['message']['from']['username'],
                   'chat_id': str(chat_id)}
            print(log)

            return {'chat_id': str(chat_id), 'text': str(text)}
        return None

    def send_message(self, chat_id, text):
        """ Sends message """
        request = self.url + f'sendmessage?chat_id={chat_id}&text={text}'
        self.r.get(request)
        return None

    def send_photo(self, chat_id, im):
        """ Sends image """
        url = self.url + 'sendPhoto'
        files = {'photo': im}
        data = {'chat_id' : chat_id}
        requests.post(url, files=files, data=data)
        return None
