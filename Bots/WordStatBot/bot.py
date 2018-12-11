#! /usr/bin/python3.5

import os
import re
from config import token
import telebot
from sql import Db
from system_func import get_ip
from system_func import is_admin
from system_func import list_to_str

bot = telebot.TeleBot(token)
db_dir = os.path.dirname(os.path.abspath(__file__)) + "/words.db"


def get_cmd_param(message, default):
    reg = re.search(r'/\w+ (\d+)', message.text)
    param = default
    if reg is not None:
        param = int(reg.group(1))
    return param


@bot.message_handler(commands=["start"])
def start(message):
    cmd_help(message)


@bot.message_handler(commands=["ip"])
def ip(message):
    bot.send_message(message.chat.id, 'Мой ip: `' + get_ip() + '`', parse_mode='Markdown')


@bot.message_handler(commands=["allwords"])
def all_words(message):
    db = Db(db_dir)
    words = db.get_frequency()
    _str = list_to_str('Топ слов', words, [0, 1])
    if _str:
        bot.send_message(message.chat.id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["topwords"])
def top_words(message):
    db = Db(db_dir)
    words = db.get_frequency_long(get_cmd_param(message, 3))
    _str = list_to_str('Топ слов', words, [0, 1])
    if _str:
        bot.send_message(message.chat.id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["mywords"])
def my_words(message):
    db = Db(db_dir)
    words = db.get_frequency_by_id(message.from_user.id, get_cmd_param(message, 3))
    _str = list_to_str('Топ слов', words, [0, 1])
    if _str:
        bot.send_message(message.chat.id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["die"])
def die(message):
    if is_admin(message):
        bot.stop_polling()


@bot.message_handler(commands=["test"])
def test(message):
    print(message)


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = '''
    Мои возможные команды:```
    help     - Показывает этот список
    mywords  - Частота употребляемых мной слов
    topwords - Самые часто употребляемые слова
    allwords - Самые часто употребляемые слова
    ```'''
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types=["text"])
def text_request(message):
    db = Db(db_dir)
    user_id = message.from_user.id
    text = re.sub(r'(http.+?\s)|(http.+$)', r' ', message.text)
    text = re.sub(r'[_+-.,!@#$%^&*();/|<>"\']', r' ', text).split()
    if text:
        for word in text:
            word = word.lower()
            if db.get_word_by_user(user_id, word):
                db.add_word(user_id, word)
            else:
                db.new_word(user_id, word)


if __name__ == '__main__':
    bot.remove_webhook()
    print('Бот работает!')
    bot.polling(none_stop=True)
