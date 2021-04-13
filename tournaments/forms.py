from django import forms
from django.shortcuts import get_object_or_404
from .models import Tournament, Team
from django.forms import ValidationError
from slugify import slugify


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
                  'contact',
                  'start_date',
                  'start_time',
                  'contact_detail',
                  'rules',
                  'schedule',
                  'prizes')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Tournament.objects.get(slug=slugify(name))
            raise ValidationError('Tournament with similar name is already exists.')
        except Team.DoesNotExist:
            pass
        return name


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',
                  'game',
                  'description',
                  'img')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        try:
            Team.objects.get(slug=slugify(name))
            raise ValidationError('Team with similar name is already exists.')
        except Team.DoesNotExist:
            pass
        return name

    def clean_game(self):
        game = self.cleaned_data.get('game')
        if not game:
            raise ValidationError('No game here')
        return game


class TeamEditForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name',
                  'img',
                  'description')
