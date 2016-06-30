CREATE TABLE sqlite_sequence
(
    name TEXT,
    seq TEXT
);
CREATE TABLE games
(
    user1 INTEGER PRIMARY KEY NOT NULL,
    user2 INTEGER,
    field TEXT DEFAULT '0000000000'
);
CREATE UNIQUE INDEX games_user1_uindex ON games (user1);
CREATE TABLE users
(
    id INTEGER PRIMARY KEY NOT NULL,
    name TEXT DEFAULT 'Unnamed' NOT NULL,
    win INTEGER DEFAULT 0,
    lose INTEGER DEFAULT 0,
    draw INTEGER DEFAULT 0,
    type INTEGER DEFAULT NULL
);
CREATE UNIQUE INDEX users_id_uindex ON users (id);