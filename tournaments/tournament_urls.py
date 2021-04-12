from django.urls import path
from . import views as v

urlpatterns = [
	path('create-torunament/', v.CreateTournament.as_view(), name='create-tournament'),
	path('create-team/', v.CreateTeam.as_view(), name='create-team'),
	path('team-list/', v.TeamList.as_view(), name='team-list'),
	path('team-deatil/<slug:slug>/', v.TeamDetail.as_view(), name='team-detail'),
	path('team-deatil/<slug:slug>/delete', v.TeamDelete.as_view(), name='team-delete'),
	path('edit-team/<slug:slug>/', v.EditTeam.as_view(), name='edit-team')
]
