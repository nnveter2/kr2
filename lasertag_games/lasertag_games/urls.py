from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('arenas/', include('arenas.urls')),
    path('games/', include('games.urls')),
]
