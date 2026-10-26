from django.urls import path

from . import views

app_name = 'games'

urlpatterns = [
    path('', views.game_list, name='list'),
    path('statistics/', views.statistics, name='statistics'),  # до slug-маршрута
    path('<slug:slug>/', views.game_detail, name='detail'),
]
