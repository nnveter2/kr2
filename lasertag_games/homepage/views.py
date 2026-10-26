from django.shortcuts import render

from games import db


def home(request):
    try:
        games = db.get_games()
    except db.DatabaseError as exc:
        print(f'DB error: {exc}')
        return render(request, 'games/error.html',
                      {'message': 'Не удалось получить данные. Попробуйте позже.'}, status=500)
    return render(request, 'homepage/home.html', {'games': games, 'games_total': db.count_games()})
