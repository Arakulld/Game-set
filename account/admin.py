from django.contrib import admin
from . import models


@admin.register(models.TournamentAccount)
class TournamentAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'phone_number')
