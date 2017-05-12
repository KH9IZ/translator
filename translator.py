import xml.dom.minidom
import telebot
import urllib
from config import *
import peewee

bot = telebot.TeleBot(token)

db = peewee.SqliteDatabase("db.sqlite")


class User(peewee.Model):
    user_id = peewee.IntegerField()
    lang = peewee.TextField()

    class Meta:
        database = db
        db_table = 'users'


@bot.message_handler(commands=['start'])
def start(message):
    #sent = bot.send_message(message.chat.id, 'Добро пожаловать в переводчик!')
    #user = User(user_id=228, lang='kek')
    #user.save()
    bot.register_next_step_handler(sent, change_language)


@bot.message_handler(commands=['lang'])
def change_language(message):
    sent = bot.send_message(message.chat.id,
                     'Введите язык на который нужно перевести в сокращении (например en или de): ')
    bot.register_next_step_handler(sent, changing)
    pass


def changing(message):
    bot.send_message(message.chat.id, 'Изменил язык на '+message.text)
    pass



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
