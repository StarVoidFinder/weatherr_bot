import requests
import config
import weatherr
import renderr
import tg_bot


def main():
    bot = tg_bot.Bot()
    weather = weatherr.Weather()
    render = renderr.Render()

    commands = {r'/current': [weather.get_current, render.make_current]}

    bot.get_message()
    print('--------------------------------')
    while True:
        answer = bot.get_message()
        if answer == None: continue

        text = answer['text']
        chat_id = answer['chat_id']


        if text in commands:
            bot.send_message(chat_id, 'Type name of city after command in one message.')
            print('<No argument>')
            print('---------')
            continue

        for command in commands:
            if text.find(command) == 0:
                flag = True

                city = text.replace(command, '').lstrip()
                data = commands[command][0](city)

                if data == None:
                    bot.send_message(chat_id, 'Your city is not found.')
                    print('<failed>')
                    print('--------')
                    continue

                im = commands[command][1](data)
                bot.send_photo(chat_id, im)

                print('<success>')
                print('---------')
                continue
                
        if flag: continue

        if '/' in text:
            bot.send_message(chat_id, 'Invalid command.')
            print('<Invalid command>')
            print('---------')
            continue


        bot.send_message(chat_id, 'Type yout request in format "/command argument."')
        print('<Invalid input>')
        print('---------')
        continue


if __name__ == '__main__':
    main()
