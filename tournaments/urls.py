from django.urls import path
from . import views as v

urlpatterns = [
	# path('create-tournament/',),
	path('team_list/', v.team_list),
	path('team_detail/', v.team_detail),
	path('games_menu/', v.games_menu),
	path('create-torunament/', v.CreateTournament.as_view(), name='create-tournament'),
	path('create_team/', v.CreateTeam.as_view(), name='create-team')
]
