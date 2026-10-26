import sqlite3
from contextlib import closing

from django.conf import settings


class DatabaseError(Exception):
    """Ошибка доступа к БД без технических подробностей для пользователя."""


# Допустимые варианты сортировки: ключ из GET -> фрагмент SQL (из белого списка)
SORT_OPTIONS = {
    'date': ('g.start_date ASC', 'по дате (сначала ранние)'),
    'date_desc': ('g.start_date DESC', 'по дате (сначала поздние)'),
    'players': ('g.players ASC', 'по игрокам (по возрастанию)'),
    'players_desc': ('g.players DESC', 'по игрокам (по убыванию)'),
    'title': ('g.title ASC', 'по названию'),
}
DEFAULT_SORT = 'date'

GAME_COLUMNS = """
    g.id, g.title, g.slug, g.game_mode, g.start_date, g.duration,
    g.players, g.status, a.name AS arena_name
"""


def _connect():
    conn = sqlite3.connect(settings.GAMES_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query(sql, params=()):
    """Выполняет параметризованный SELECT и возвращает список словарей."""
    try:
        with closing(_connect()) as conn:
            cursor = conn.execute(sql, params)
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as exc:
        raise DatabaseError(str(exc)) from exc


def count_games():
    return query('SELECT COUNT(*) AS total FROM games')[0]['total']


def get_arenas():
    return query(
        'SELECT id, name, capacity, arena_kind FROM arenas ORDER BY name'
    )


def get_games(min_players=0, sort=DEFAULT_SORT, limit=None):
    order_by = SORT_OPTIONS.get(sort, SORT_OPTIONS[DEFAULT_SORT])[0]
    sql = (
        f'SELECT {GAME_COLUMNS} FROM games g '
        'LEFT JOIN arenas a ON a.id = g.arena_id '
        'WHERE g.players >= ? '
        f'ORDER BY {order_by}'
    )
    params = [min_players]
    if limit is not None:
        sql += ' LIMIT ?'
        params.append(limit)
    return query(sql, params)


def get_game_by_slug(slug):
    rows = query(
        f"""SELECT {GAME_COLUMNS},
                   a.capacity AS arena_capacity, a.arena_kind
            FROM games g
            LEFT JOIN arenas a ON a.id = g.arena_id
            WHERE g.slug = ?""",
        (slug,),
    )
    return rows[0] if rows else None


def get_mode_statistics(min_count=2):
    return query(
        """SELECT game_mode, COUNT(*) AS games_count
           FROM games
           GROUP BY game_mode
           HAVING COUNT(*) >= ?
           ORDER BY games_count DESC, game_mode""",
        (min_count,),
    )
