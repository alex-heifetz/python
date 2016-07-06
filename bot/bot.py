#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import telebot
import tokens
from telebot import types
from sql import Db
import random
import os

db_dir = os.path.dirname(os.path.abspath(__file__)) + "/db.db"


def draw_field(field):
    str_ = '<pre>'
    str_ += '\n┏---┳---┳---┓\n'
    for i in [0, 1, 2]:
        for j in [1, 2, 3]:
            pos = i * 3 + j
            str_ += '┃'
            if '0' == field[pos]:
                sym = ' '
            else:
                sym = field[pos]
            str_ += ' ' + sym + ' '
        str_ += "┃"
        if 2 != i:
            str_ += "\n┣---╋---╋---┫\n"
        else:
            str_ += "\n┗---┻---┻---┛\n"
    str_ += '</pre>'
    return str_


# def draw_field(field):
#     str_ = '<pre>'
#     str_ += '\n┏━━━┳━━━┳━━━┓\n'
#     for i in [0, 1, 2]:
#         for j in [1, 2, 3]:
#             pos = i * 3 + j
#             str_ += '┃'
#             if '0' == field[pos]:
#                 sym = ' '
#             else:
#                 sym = field[pos]
#             str_ += ' ' + sym + ' '
#         str_ += "┃"
#         if 2 != i:
#             str_ += "\n┣━━━╋━━━╋━━━┫\n"
#         else:
#             str_ += "\n┗━━━┻━━━┻━━━┛\n"
#     str_ += '</pre>'
#     return str_


def other_type(type_):
    if 'X' == type_:
        return 'O'
    else:
        return 'X'


def check_can_win_lose(field, type_):
    user = other_type(type_)
    lose_pos = False
    win_pos = False
    for i in [0, 1, 2]:
        for j in [1, 2, 3]:
            pos = i * 3 + j
            if '0' == field[pos]:
                field_win = field[:pos] + type_ + field[pos + 1:]
                field_lose = field[:pos] + user + field[pos + 1:]
                win = check_win(field_win, type_)
                lose = check_win(field_lose, user)
                if lose:
                    lose_pos = pos
                if win:
                    win_pos = pos
    if win_pos:
        return win_pos
    if lose_pos:
        return lose_pos
    return False


def bot_step(user_id, field):
    db = Db(db_dir)
    user = str(db.get_user_by_id(user_id)[1])
    type_ = other_type(user)
    right_step = check_can_win_lose(field, type_)
    if right_step:
        return db.set_step(user_id, right_step, True)
    # if '0' == field[5]:
    #     return db.set_step(user_id, 5, True)
    while True:
        pos = random.randint(1, 9)
        if '0' == field[pos]:
            return db.set_step(user_id, pos, True)


def check_win(f, type_):
    return f[1] == f[2] == f[3] == type_ or \
           f[4] == f[5] == f[6] == type_ or \
           f[7] == f[8] == f[9] == type_ or \
           f[1] == f[4] == f[7] == type_ or \
           f[2] == f[5] == f[8] == type_ or \
           f[3] == f[6] == f[9] == type_ or \
           f[1] == f[5] == f[9] == type_ or \
           f[3] == f[5] == f[7] == type_


def who_win(field):
    n = 0
    for i in field:
        if i in ['X', 'O']:
            n += 1
    if 9 == n:
        return "Ничья"
    if check_win(field, 'X'):
        return 'X победили!'
    if check_win(field, 'O'):
        return 'O победили!'
    return False


bot = telebot.TeleBot(tokens.token)


@bot.message_handler(commands=["help"])
def repeat_all_messages(message):
    text = '''
    Мои возможные команды:
     - /help Показывает этот список
     - /register Добавляет вас в список игроков
     - /start Начинает игру в крестики нолики с тупом ботом
     - /end Принудительно заканчивает игру
     - /top Показывает топ игроков
    '''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["register"])
def repeat_all_messages(message):
    db = Db(db_dir)
    user = db.get_user_by_id(message.chat.id)
    if not user:
        if message.chat.username:
            db.add_user(message.chat.id, message.chat.username)
        elif message.chat.first_name:
            db.add_user(message.chat.id, message.chat.first_name)
        else:
            bot.send_message(message.chat.id, "У Вас нету имени, бот не может Вас зарегистрировать!")
        bot.send_message(message.chat.id, "Поздравляем с регистрацией!")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы!")


@bot.message_handler(commands=["top"])
def repeat_all_messages(message):
    db = Db(db_dir)
    res = db.get_top_10()
    if res:
        str_ = '<strong>Имя, побед/всего, процент побед:</strong>\n'
        for user in res:
            if None is not user[3]:
                str_ += '<b>' + str(user[0]) + '</b>: ' + str(user[1]) + '/' + str(user[2]) + ' ' + str(
                    round(user[3], 2)) + '\n'
        if '<strong>Имя, побед/всего, процент побед:</strong>\n' != str_:
            bot.send_message(message.chat.id, str(str_), parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, 'Статистики пока что нет')


@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    user_id = message.chat.id
    db = Db(db_dir)
    user = db.get_user_by_id(user_id)
    if not user:
        bot.send_message(user_id, "Вам нужно зарегистрироваться командой: /register")
    else:
        game_ = db.get_game(user_id)
        if not game_:
            markup = types.ReplyKeyboardMarkup()
            markup.row('X', 'O')
            bot.send_message(user_id, "Выбирите Х или О:", reply_markup=markup)
        else:
            game(message)


@bot.message_handler(commands=["end"])
def end_game(message):
    user_id = message.chat.id
    db = Db(db_dir)
    user = db.get_user_by_id(user_id)
    if not user:
        return False
    if user[5]:
        markup = types.ReplyKeyboardHide()
        db.set_type_to_user(user_id, None)
        db.end_game(user_id)
        bot.send_message(message.chat.id, "Игра окончена!", reply_markup=markup)


def game(message):
    user_id = message.chat.id
    db = Db(db_dir)
    user = db.get_user_by_id(user_id)
    if user[1]:
        markup = types.ReplyKeyboardMarkup()
        markup.row('1', '2', '3')
        markup.row('4', '5', '6')
        markup.row('7', '8', '9')
        bot.send_message(message.chat.id, "Ваш ход:", reply_markup=markup)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    user_id = message.chat.id
    db = Db(db_dir)
    user = db.get_user_by_id(user_id)
    if user:
        if user[1]:
            if message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                pos = int(message.text)
                user_game = db.get_game(user_id)
                if '0' == user_game[2][pos]:
                    field = db.set_step(user_id, pos)
                    winner = who_win(field)
                    if winner:
                        markup = types.ReplyKeyboardHide()
                        field = draw_field(field)
                        bot.send_message(user_id, field + "\n" + winner, reply_markup=markup, parse_mode='HTML')
                        db.set_type_to_user(user_id, None)
                        if 'Ничья' == winner:
                            db.user_draw(user_id)
                        else:
                            db.user_win(user_id)
                        db.end_game(user_id)
                        return True
                    field = bot_step(user_id, field)
                    winner = who_win(field)
                    if winner:
                        markup = types.ReplyKeyboardHide()
                        field = draw_field(field)
                        bot.send_message(user_id, field + "\n" + winner, reply_markup=markup, parse_mode='HTML')
                        db.set_type_to_user(user_id, None)
                        if 'Ничья' == winner:
                            db.user_draw(user_id)
                        else:
                            db.user_lose(user_id)
                        db.end_game(user_id)
                        return True
                    field = draw_field(field)
                    bot.send_message(user_id, field, parse_mode='HTML')
                else:
                    bot.send_message(user_id, 'Так сходить нельзя')
            else:
                markup = types.ReplyKeyboardHide()
                if message.text in ['X', 'O']:
                    db.set_type_to_user(user_id, message.text)
                    bot.send_message(user_id, 'Вы выбрали ' + str(message.text) + '!', reply_markup=markup)
                db.create_game(user_id)
                game(message)


if __name__ == '__main__':
    # bot.remove_webhook()
    print "Бот работает!"
    bot.polling(none_stop=True)
