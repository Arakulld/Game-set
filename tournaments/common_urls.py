from django.urls import path
from . import views as v

urlpatterns = [
    path('', v.IndexView.as_view(), name='index'),
    path('team/join/<str:token>/', v.JoinTeam.as_view(), name='join-team'),
]
