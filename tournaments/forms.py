from django import forms
from django.forms import ValidationError
from .models import Tournament
from .models import Game
from .models import GameFormat


class TournamentCreateForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name',
                  'description',
                  'img',
                  'game',
                  'game_format',
                  'max_participants',
                  'communication',
                  'contact_detail',
                  'start_date',
                  'start_time')

