#!/usr/bin/python3.5
import json
import tokens
import telebot
import callbacks_actions
from sql import Db
from random import shuffle
from telebot import types
from options import chat_id
from options import db_dir
from system_func import get_ip
from system_func import is_admin
from system_func import list_to_str

bot = telebot.TeleBot(tokens.token)


@bot.message_handler(commands=["start"])
def start(message):
    cmd_help(message)


@bot.message_handler(commands=["register"])
def register(message):
    db = Db(db_dir)
    user = db.get_user_by_id(message.from_user.id)
    if not user:
        if message.from_user.username:
            db.add_user(message.from_user.id, message.from_user.username)
        elif message.from_user.first_name:
            db.add_user(message.from_user.id, message.from_user.first_name)
        else:
            bot.send_message(chat_id, "У Вас нету имени, бот не может Вас зарегистрировать!")
        bot.send_message(chat_id, "Поздравляем с регистрацией!")
    else:
        print(user)
        # bot.send_message(chat_id, "Вы уже зарегистрированы!")


@bot.message_handler(commands=["list"])
def place_list(message):
    db = Db(db_dir)
    places = db.get_places()
    _str = list_to_str('Список мест', places, [1])
    if _str:
        bot.send_message(chat_id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["listavailable"])
def place_list_for_random(message):
    db = Db(db_dir)
    places = db.get_places_for_random()
    _str = list_to_str('Список возможных мест на сегодня мест', places, [1])
    if _str:
        bot.send_message(chat_id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["random"])
def random(message):
    db = Db(db_dir)
    today = db.get_today_crusade()
    if today:
        bot.send_message(chat_id, 'Сегодня уже выбран - ' + str(today[0][0]))
    else:
        places = db.get_places_for_random()
        shuffle(places)
        db.add_crusade(places[0][0])
        bot.send_message(chat_id, 'Выбор на сегодня - ' + str(places[0][1]))


@bot.message_handler(commands=["delete"])
def random(message):
    if is_admin(message):
        db = Db(db_dir)
        db.delete_today()


@bot.message_handler(commands=["crusades"])
def crusades(message):
    db = Db(db_dir)
    _crusades = db.get_crusades()
    _str = list_to_str('Топ слов', _crusades, [1, 0])
    if _str:
        bot.send_message(chat_id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["ip"])
def ip(message):
    bot.send_message(chat_id, 'Мой ip: `' + get_ip() + '`', parse_mode='Markdown')


@bot.message_handler(commands=["softdelete"])
def softdelete(message):
    if is_admin(message):
        db = Db(db_dir)
        places = db.get_all_places()
        if places:
            keyboard = types.InlineKeyboardMarkup()
            for place in places:
                if 1 == place[3]:
                    status = '👍'
                else:
                    status = '👎'
                place_button = types.InlineKeyboardButton(text=str(place[1]) + ' ' + status,
                                                          callback_data=u'{"action": "delete", "id": "' + str(
                                                              place[0]) + '"}')
                keyboard.add(place_button)
            bot.send_message(chat_id, "Выберите место чтобы удалить или добавить:", reply_markup=keyboard)


@bot.message_handler(commands=["change"])
def change(message):
    if is_admin(message):
        db = Db(db_dir)
        places = db.get_places()
        if places:
            keyboard = types.InlineKeyboardMarkup()
            for place in places:
                place_button = types.InlineKeyboardButton(text=str(place[1]),
                                                          callback_data=u'{"action": "change", "id": "' + str(
                                                              place[0]) + '"}')
                keyboard.add(place_button)
            bot.send_message(chat_id, "Выберите место на сегодня:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    print(call)
    if is_admin(call):
        msg_id = call.message.message_id
        data = json.loads(call.data)
        if 'change' == data['action']:
            place_name = callbacks_actions.change(call.message, data['id'])
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id,
                                  text="Вы выбрали: " + place_name)

        if 'delete' == data['action']:
            place_name = callbacks_actions.delete(call.message, data['id'])
            bot.edit_message_text(chat_id=chat_id, message_id=msg_id,
                                  text="Вы выбрали: " + place_name)


@bot.message_handler(commands=["topword"])
def topword(message):
    db = Db(db_dir)
    words = db.get_frequency()
    _str = list_to_str('Топ слов', words, [0, 1])
    if _str:
        bot.send_message(chat_id, str(_str), parse_mode='HTML')


@bot.message_handler(commands=["die"])
def die(message):
    if is_admin(message):
        bot.stop_polling()


@bot.message_handler(commands=["test"])
def test(message):
    print('Test')


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = '''
    Мои возможные команды:```
    help          - Показывает этот список
    random        - Рандомное место
    change        - Поменять место
    list          - Показывает список мест
    listavailable - Показывает список мест на сегодня
    crusades      - Список всех походов
    topword       - Самые часто употребляемые слова
    ip            - Возвращает IP
    register      - Регистрирует пользователя
    test          - Что-то для отладки
    ```'''
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types=["text"])
def text_request(message):
    db = Db(db_dir)
    user_id = message.from_user.id
    text = message.text.split()
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
