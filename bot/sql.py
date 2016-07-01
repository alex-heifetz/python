# -*- coding: utf-8 -*-

import sqlite3


class Db:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_users(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users').fetchall()

    def get_top_10(self):
        with self.connection:
            return self.cursor.execute(
                'SELECT name, win, (win+lose+draw) AS col, CAST(win AS FLOAT)/CAST((win+lose) AS FLOAT)*100 AS winrate FROM users ORDER BY winrate DESC LIMIT 10').fetchall()

    def get_user_by_id(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()

    def add_user(self, user_id, name):
        with self.connection:
            if name:
                return self.cursor.execute('INSERT INTO users VALUES (?, ?, 0, 0, 0, ?)', (user_id, name, None))

    def set_type_to_user(self, user_id, type_):
        with self.connection:
            return self.cursor.execute('UPDATE users SET type = ? WHERE id = ?', (type_, user_id))

    def user_win(self, user_id):
        with self.connection:
            win = 1 + self.cursor.execute('SELECT win FROM users WHERE id = ?', (user_id,)).fetchone()[0]
            bot_lose = 1 + self.cursor.execute('SELECT lose FROM users WHERE id = 1').fetchone()[0]
            self.cursor.execute('UPDATE users SET lose = ? WHERE id = 1', (bot_lose,))
            return self.cursor.execute('UPDATE users SET win = ? WHERE id = ?', (win, user_id))

    def user_lose(self, user_id):
        with self.connection:
            lose = 1 + self.cursor.execute('SELECT lose FROM users WHERE id = ?', (user_id,)).fetchone()[0]
            bot_win = 1 + self.cursor.execute('SELECT win FROM users WHERE id = 1').fetchone()[0]
            self.cursor.execute('UPDATE users SET win = ? WHERE id = 1', (bot_win,))
            return self.cursor.execute('UPDATE users SET lose = ? WHERE id = ?', (lose, user_id))

    def user_draw(self, user_id):
        with self.connection:
            draw = 1 + self.cursor.execute('SELECT draw FROM users WHERE id = ?', (user_id,)).fetchone()[0]
            bot_draw = 1 + self.cursor.execute('SELECT draw FROM users WHERE id = 1').fetchone()[0]
            self.cursor.execute('UPDATE users SET draw = ? WHERE id = 1', (bot_draw,))
            return self.cursor.execute('UPDATE users SET draw = ? WHERE id = ?', (draw, user_id))

    def create_game(self, user_id):
        with self.connection:
            return self.cursor.execute('INSERT INTO games VALUES (?, 1, "0000000000")', (user_id,))

    def get_game(self, user_id):
        with self.connection:
            return self.cursor.execute('SELECT * FROM games WHERE user1 = ?', (user_id,)).fetchone()

    def set_step(self, user_id, pos, bot=False):
        with self.connection:
            field = str(self.cursor.execute('SELECT field FROM games WHERE user1 = ?', (user_id,)).fetchone()[0])
            type_ = str(self.cursor.execute('SELECT type FROM users WHERE id = ?', (user_id,)).fetchone()[0])
            if bot:
                if 'X' == type_:
                    type_ = 'O'
                else:
                    type_ = 'X'
            field = str(int(field[0]) + 1) + field[1:pos] + type_ + field[pos + 1:]
            self.cursor.execute('UPDATE games SET field = ? WHERE user1 = ?', (field, user_id))
            return field

    def end_game(self, user_id):
        with self.connection:
            return self.cursor.execute('DELETE FROM games WHERE user1 = ?', (user_id,))

    def close(self):
        self.connection.close()
