from django.urls import path
from . import views as v

urlpatterns = [
	path('create_tournaments/', v.create_tournaments, name='create_tournaments'),
	path('dandelions/', v.dandelions, name='dandelions'),
	path('games_menu/', v.games_menu, name='games_menu'),
]
