#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import conf
import os
import subprocess
from status import global_status

dir_ = os.path.dirname(os.path.abspath(__file__))

bot = telebot.TeleBot(conf.token)
my_id = conf.my_id


def do_action(action, message):
    l = len(action) + 2
    if message.text[l:]:
        markup = types.ReplyKeyboardHide()
        bot.send_message(message.chat.id, 'Процесс запущен: vagrant ' + action + ' ' + str(message.text[l:l + 7]),
                         reply_markup=markup)
        subprocess.Popen('vagrant ' + action + ' ' + message.text[l:l + 7], shell=True,
                         stdout=subprocess.PIPE).communicate()
    else:
        boxs = global_status(action)
        res = ''
        if boxs:
            markup = types.ReplyKeyboardMarkup()
            for boxid, name in boxs.items():
                res += str(boxid) + ' ' + str(name) + "\n"
                markup.row('/' + action + ' ' + str(boxid) + ' ' + str(name))
            bot.send_message(message.chat.id, '<pre>' + res + '</pre>', parse_mode='HTML', reply_markup=markup)


@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    cmd_help(message)


@bot.message_handler(commands=["die"])
def repeat_all_messages(message):
    if my_id == message.chat.id:
        bot.stop_polling()


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = '''
    Мои возможные команды:
     - /help Показывает этот список
     - /status Результат команды `vagrant global-status`

    Команды типа:
     - /<action> Предлогает варианты машин над которыми <action> возможен
     - /<action> <id> Выполняет `vagrant <action> <id>`
    Список <action>:
     - up Запустить
     - suspend Усыпить
     - reload Перезапустить
     - halt Выключить
     - destroy Уничтожить
    '''
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(commands=["status"])
def cmd_status(message):
    if my_id == message.chat.id:
        vgs = global_status('status')
        new_vgs = ''
        for key in vgs:
            new_vgs += key + ' ' + vgs[key] + "\n"
        bot.send_message(message.chat.id, '<pre>' + new_vgs + '</pre>', parse_mode='HTML')


@bot.message_handler(commands=["up"])
def cmd_up(message):
    if my_id == message.chat.id:
        do_action('up', message)


@bot.message_handler(commands=["halt"])
def cmd_halt(message):
    if my_id == message.chat.id:
        do_action('halt', message)


@bot.message_handler(commands=["suspend"])
def cmd_suspend(message):
    if my_id == message.chat.id:
        do_action('suspend', message)


@bot.message_handler(commands=["reload"])
def cmd_reload(message):
    if my_id == message.chat.id:
        do_action('reload', message)


@bot.message_handler(commands=["destroy"])
def cmd_destroy(message):
    if my_id == message.chat.id:
        do_action('destroy', message)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.remove_webhook()
    subprocess.Popen('vagrant global-status --prune', shell=True, stdout=subprocess.PIPE).communicate()
    bot.send_message(my_id, 'I\'m alive!')
    subprocess.Popen('notify-send "Vagrant Bot Up"', shell=True, stdout=subprocess.PIPE).communicate()
    print "Бот работает!"
    bot.polling(none_stop=True)
