from django.urls import path

from . import views

app_name = 'arenas'

urlpatterns = [path('', views.arena_list, name='list')]
