#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import telebot
import tokens
import os
import subprocess
import urllib2
from menu import pls_parse_this_shit

dir_ = os.path.dirname(os.path.abspath(__file__))
www250 = 'http://www.brandmeister.spb.ru/menu/biznes-lanch#content'
www300 = 'http://www.brandmeister.spb.ru/menu/premium-lanchi-300-rub#content'

bot = telebot.TeleBot(tokens.token)


@bot.message_handler(commands=["start"])
def repeat_all_messages(message):
    cmd_help(message)


@bot.message_handler(commands=["die"])
def repeat_all_messages(message):
    if 217193856 == message.chat.id:
        bot.stop_polling()


@bot.message_handler(commands=["help"])
def cmd_help(message):
    text = '''
    Мои возможные команды:
     - /help Показывает этот список
     - /menu Показывает меню кафе "Бранд-Мейстер"
    '''
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["menu"])
def cmd_menu(message):
    response250 = urllib2.urlopen(www250)
    response300 = urllib2.urlopen(www300)
    if message.text[6:]:
        price = message.text[6:]
        if '250' == price:
            text = pls_parse_this_shit(response250)
        if '300' == price:
            text = pls_parse_this_shit(response300)
        if text:
            bot.send_message(message.chat.id, text, parse_mode='HTML')

    else:
        text = pls_parse_this_shit(response250)
        bot.send_message(message.chat.id, text, parse_mode='HTML')
        text = pls_parse_this_shit(response300)
        bot.send_message(message.chat.id, text, parse_mode='HTML')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    # bot.remove_webhook()
    print "Бот работает!"
    response250 = urllib2.urlopen(www250)
    response300 = urllib2.urlopen(www300)
    text = pls_parse_this_shit(response250)
    bot.send_message(39153112, text, parse_mode='HTML')
    bot.send_message(217193856, text, parse_mode='HTML')
    text = pls_parse_this_shit(response300)
    bot.send_message(39153112, text, parse_mode='HTML')
    bot.send_message(217193856, text, parse_mode='HTML')
    bot.polling(none_stop=True)
