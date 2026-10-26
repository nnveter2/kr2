from django.shortcuts import render

from games import db


def arena_list(request):
    try:
        arenas = db.get_arenas()
    except db.DatabaseError as exc:
        print(f'DB error: {exc}')
        return render(request, 'games/error.html',
                      {'message': 'Не удалось получить данные. Попробуйте позже.'}, status=500)
    return render(request, 'arenas/arena_list.html', {'arenas': arenas})
