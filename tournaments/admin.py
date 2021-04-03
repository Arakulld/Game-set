from django.contrib import admin
from . import models


@admin.register(models.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(models.GameFormat)
class GameFormatAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'game', 'max_players')


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
