import urllib
import xml.dom.minidom

import telebot
from config import *

bot = telebot.TeleBot(token)


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_answer(query):
    text = query.query
    lang = 'ru'
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
    ans = telebot.types.InlineQueryResultArticle(
        id='0',
        title=text.childNodes[0].nodeValue,
        input_message_content=telebot.types.InputTextMessageContent(text.childNodes[0].nodeValue)
    )
    bot.answer_inline_query(query.id, [ans])


@bot.message_handler(func=lambda message: message.text not in ('ru', 'en', 'de'))
def translate(message):
    text = message.text
    lang = 'ru'
    for i in text:
        if ((i > 'a') and (i < 'z')) or ((i > 'A') and (i < 'Z')):
            lang = 'ru'
        else:
            lang = 'en'
        break
    print(message)
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
