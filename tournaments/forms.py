from django import forms
from django.forms import ValidationError
from .models import Tournament, Team
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


class TeamCreateForm(forms.ModelForm):

    def __init__(self, user=None, *args, **kwargs):
        super(TeamCreateForm, self).__init__(*args, **kwargs)
        if user:
            self.owner = user

    class Meta:
        model = Team
        fields = ('owner',
                  'name',
                  'game',
                  'description',
                  'img')
