#! /usr/bin/python3.5
# -*- coding: utf-8 -*-

import os
import sqlite3


class Db:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def migrate(self):
        with self.connection:
            return self.cursor.execute(
                'CREATE TABLE words (id INTEGER PRIMARY KEY AUTOINCREMENT, word STRING, user_id INTEGER, count INTEGER)')


db_dir = os.path.dirname(os.path.abspath(__file__)) + "/words.db"
db = Db(db_dir)
db.migrate()
