# -*- coding: utf-8 -*-
import sqlite3


class Db:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_users(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users').fetchall()

    def get_user_by_id(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    def add_user(self, user_id, name):
        with self.connection:
            if name:
                return self.cursor.execute('INSERT INTO users VALUES (?, ?)', (user_id, name))

    def change_point(self, user_name, dif):
        with self.connection:
            if '+' == dif:
                return self.cursor.execute('UPDATE users SET points = points + 1 WHERE name = ?', (user_name,))
            if '-' == dif:
                return self.cursor.execute('UPDATE users SET points = points - 1 WHERE name = ?', (user_name,))

    def get_top(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users ORDER BY points DESC').fetchall()

    def get_all_places(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM places').fetchall()

    def get_places(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM places WHERE `delete` = 0').fetchall()

    def get_place(self, place_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM places WHERE `id` = ?', (place_id,)).fetchone()

    def get_places_for_random(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT * FROM places WHERE `delete` = 0 AND places.id NOT IN (SELECT place_id FROM CRUSADES ORDER BY date DESC LIMIT 5)').fetchall()

    def set_delete(self, place_id, status):
        with self.connection:
            print(place_id)
            print(status)
            return self.cursor.execute('UPDATE places SET `delete` = ? WHERE `id` = ?', (status, place_id))

    def delete_today(self):
        with self.connection:
            return self.cursor.execute('DELETE FROM crusades WHERE date = date(\'now\', \'+3 hours\')')

    def get_crusades(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT places.name, crusades.date FROM crusades JOIN places ON crusades.place_id = places.id ORDER BY date DESC LIMIT 10').fetchall()

    def get_today_crusade(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT places.name, crusades.date FROM crusades JOIN places ON crusades.place_id = places.id WHERE date = date(\'now\', \'+3 hours\')').fetchall()

    def add_crusade(self, place_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO crusades VALUES (?, strftime(\'%Y-%m-%d\',\'now\', \'+3 hours\'))',
                                       (place_id,))

    def update_crusade(self, place_id):
        with self.connection:
            return self.cursor.execute(
                'UPDATE crusades SET place_id = ? WHERE date = strftime(\'%Y-%m-%d\',\'now\', \'+3 hours\')',
                (place_id,))

    def get_word(self, word):
        with self.connection:
            return self.cursor.execute('SELECT * FROM words WHERE word = ?', (word,)).fetchall()

    def get_word_by_user(self, user_id, word):
        with self.connection:
            return self.cursor.execute('SELECT * FROM words WHERE word = ? AND user_id = ?', (word, user_id)).fetchall()

    def new_word(self, user_id, word):
        with self.connection:
            return self.cursor.execute('INSERT INTO words (word, user_id, count) VALUES (?, ?, 1)', (word, user_id))

    def add_word(self, user_id, word):
        with self.connection:
            return self.cursor.execute('UPDATE words SET count = count + 1 WHERE word = ? AND user_id = ?',
                                       (word, user_id))

    def get_frequency(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT word, SUM(count) AS count FROM words GROUP BY word ORDER BY count DESC LIMIT 10').fetchall()

    def close(self):
        self.connection.close()
