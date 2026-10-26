-- Схема
CREATE TABLE arenas (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT    NOT NULL,
    capacity   INTEGER NOT NULL,
    arena_kind TEXT    NOT NULL
);

CREATE TABLE games (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    title      TEXT    NOT NULL,
    slug       TEXT    NOT NULL UNIQUE,
    game_mode  TEXT    NOT NULL,
    start_date TEXT    NOT NULL,
    duration   INTEGER NOT NULL,
    players    INTEGER NOT NULL,
    status     TEXT    NOT NULL,
    arena_id   INTEGER REFERENCES arenas(id)
);

-- Список арен
SELECT id, name, capacity, arena_kind FROM arenas ORDER BY name;

-- Количество игр
SELECT COUNT(*) AS total FROM games;

-- Список игр с ареной (JOIN, ORDER BY, LIMIT, фильтр по минимуму игроков)
SELECT g.id, g.title, g.slug, g.game_mode, g.start_date, g.duration,
       g.players, g.status, a.name AS arena_name
FROM games g
LEFT JOIN arenas a ON a.id = g.arena_id
WHERE g.players >= ?
ORDER BY g.start_date ASC
LIMIT ?;

-- Игра по slug вместе с данными арены
SELECT g.id, g.title, g.slug, g.game_mode, g.start_date, g.duration,
       g.players, g.status, a.name AS arena_name,
       a.capacity AS arena_capacity, a.arena_kind
FROM games g
LEFT JOIN arenas a ON a.id = g.arena_id
WHERE g.slug = ?;

-- Статистика: режимы, в которых не меньше N игр
SELECT game_mode, COUNT(*) AS games_count
FROM games
GROUP BY game_mode
HAVING COUNT(*) >= ?
ORDER BY games_count DESC, game_mode;
