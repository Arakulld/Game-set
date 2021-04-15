from django.contrib import admin
from . import models


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'name', 'slug', 'get_game', 'img')

    def get_game(self, obj: models.Team):
        return obj.game.name


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(models.GameFormat)
class GameFormatAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'img')
    prepopulated_fields = {'slug': ('name',)}
