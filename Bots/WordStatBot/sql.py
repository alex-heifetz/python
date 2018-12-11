# -*- coding: utf-8 -*-
import sqlite3


class Db:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

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

    def get_frequency_long(self, _len):
        with self.connection:
            return self.cursor.execute(
                "SELECT word, SUM(count) AS count " +
                "FROM words " +
                "WHERE LENGTH(word)>=? " +
                "GROUP BY word " +
                "ORDER BY count DESC " +
                "LIMIT 10",
                (_len,)).fetchall()

    def get_frequency_by_id(self, user_id, _len):
        with self.connection:
            return self.cursor.execute(
                'SELECT word, SUM(count) AS count ' +
                'FROM words ' +
                'WHERE user_id=? AND LENGTH(word)>=? ' +
                'GROUP BY word ' +
                'ORDER BY count DESC ' +
                'LIMIT 10',
                (user_id, _len)).fetchall()

    def close(self):
        self.connection.close()
