from datetime import datetime

from django.http import Http404
from django.shortcuts import render

from . import db

STATS_MIN_COUNT = 2
MAX_LIMIT = 100


def _int_param(request, name, default, minimum=0):
    """Читает целочисленный GET-параметр; при некорректном значении — default."""
    raw = request.GET.get(name, '').strip()
    try:
        return max(int(raw), minimum)
    except ValueError:
        return default


def _parse_dates(games):
    return [
        {**game, 'start_date': datetime.strptime(game['start_date'], '%Y-%m-%d %H:%M')}
        for game in games
    ]


def _db_error(request, exc):
    print(f'DB error: {exc}')  # подробности только в логе сервера
    return render(
        request,
        'games/error.html',
        {'message': 'Не удалось получить данные. Попробуйте позже.'},
        status=500,
    )


def game_list(request):
    min_players = _int_param(request, 'players', 0)
    limit = _int_param(request, 'limit', None, minimum=1)
    if limit is not None:
        limit = min(limit, MAX_LIMIT)
    sort = request.GET.get('sort', db.DEFAULT_SORT)
    if sort not in db.SORT_OPTIONS:
        sort = db.DEFAULT_SORT
    try:
        games = _parse_dates(db.get_games(min_players, sort, limit))
    except db.DatabaseError as exc:
        return _db_error(request, exc)
    context = {
        'games': games,
        'min_players': min_players,
        'limit': limit or '',
        'sort': sort,
        'sort_options': [(key, label) for key, (_, label) in db.SORT_OPTIONS.items()],
    }
    return render(request, 'games/game_list.html', context)


def game_detail(request, slug):
    try:
        game = db.get_game_by_slug(slug)
    except db.DatabaseError as exc:
        return _db_error(request, exc)
    if game is None:
        raise Http404('Игра не найдена')
    game = _parse_dates([game])[0]
    return render(request, 'games/game_detail.html', {'game': game})


def statistics(request):
    min_count = _int_param(request, 'min', STATS_MIN_COUNT, minimum=1)
    try:
        stats = db.get_mode_statistics(min_count)
    except db.DatabaseError as exc:
        return _db_error(request, exc)
    return render(request, 'games/statistics.html', {'stats': stats, 'min_count': min_count})
