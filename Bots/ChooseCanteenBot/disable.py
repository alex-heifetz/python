@bot.message_handler(commands=["points"])
def points(message):
    if is_admin(message):
        db = Db(db_dir)
        users = db.get_users()
        if users:
            markup = types.ReplyKeyboardMarkup()
            for user in users:
                markup.row(str(user[1]) + ' -', str(user[2]), str(user[1]) + ' +')
            markup.row('Закончить')
            bot.send_message(message.from_user.id, "Выберите действие", reply_markup=markup)


@bot.message_handler(commands=["top"])
def top(message):
    db = Db(db_dir)
    top = db.get_top()
    if top:
        str_ = '<strong>Топ:</strong>\n'
        for user in top:
            str_ += str(user[1]) + ' - ' + str(user[2]) + '\n'
        bot.send_message(chat_id, str(str_), parse_mode='HTML')


@bot.message_handler(content_types=["text"])
def text_request(message):
    db = Db(db_dir)
    user_id = message.from_user.id;
    text = message.text.split()
    if text:
        for word in text:
            word = word.lower()
            if db.get_word_by_user(user_id, word):
                db.add_word(user_id, word)
            else:
                db.new_word(user_id, word)
    if message.chat.id != chat_id and is_admin(message):
        if 'Закончить' == message.text:
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.from_user.id, 'Ок', reply_markup=markup)
        else:
            user_name = re.sub(' [-+].*', '', message.text)
            dif = message.text[-1]
            if user_name and dif:
                db.change_point(user_name, dif)
                points(message)


@bot.message_handler(commands=["force"])
def force():
    db = Db(db_dir)
    places = db.get_places_for_random()
    shuffle(places)
    bot.send_message(chat_id, 'Рандом на сегодня - ' + str(places[0][1]))
