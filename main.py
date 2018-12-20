import requests   
import config        
import weatherr


class Bot:
    def __init__(self):
        """ Initialization """
        self.token = config.tokens['bot']
        self.url = 'https://api.telegram.org/bot' + self.token + '/'
        self.r = requests
        self.last_update = None

    def get_html(self, url):
        """ Gets html from webpage """
        return self.r.get(url).json()
    
    def get_updates(self):
        """ Gets updates from telegram """
        request = self.url + 'getUpdates'
        return self.get_html(request)

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


def main():
    bot = Bot()
    weather = weatherr.Weather()

    while True:
        answer = bot.get_message()
        if not answer == None:

            text = weather.get_current(answer['text'])
            if not text == None:
                bot.send_message(answer['chat_id'], text)
            else:
                bot.send_message(answer['chat_id'], 'Введи правильный город')


if __name__ == '__main__':
    main()