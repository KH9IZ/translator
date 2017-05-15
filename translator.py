import xml.dom.minidom
import telebot
import urllib
from config import *
import peewee

bot = telebot.TeleBot(token)


@bot.message_handler(content_types=['text'])
def translate(message):
    print(message)
    text = message.text
    for i in text:
        if ((i > 'a') and (i < 'z')) or ((i > 'A') and (i < 'Z')):
            lang = 'ru'
        else:
            lang = 'en'
        break
    print(lang)
    args = {'key': key, 'text': text, 'lang': lang}
    enc_args = urllib.parse.urlencode(args)
    response = urllib.request.urlopen('https://translate.yandex.net/api/v1.5/tr/translate?' + enc_args)
    xml_file = response.read()
    xml_file = xml_file.decode('utf-8')
    dom = xml.dom.minidom.parseString(xml_file)
    dom.normalize()
    text = dom.getElementsByTagName("text")[0]

    bot.send_message(message.chat.id, text.childNodes[0].nodeValue)


if __name__ == '__main__':
    bot.polling(none_stop=True)
db.close()
