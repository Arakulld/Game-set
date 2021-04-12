from django.db import models
from django.conf import settings
from slugify import slugify
from django.urls import reverse
import os


class JoinLink(models.Model):
    team = models.OneToOneField('Team', related_name='join_link', on_delete=models.CASCADE)
    link = models.CharField(max_length=256)


class Team(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_teams')
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    game = models.ForeignKey('Game', related_name='teams', on_delete=models.CASCADE)
    description = models.TextField()
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teams', blank=True)
    tournaments = models.ManyToManyField('Tournament', related_name='teams_registered', blank=True)

    img = models.ImageField(upload_to='tournaments', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.img:
            try:
                old = Team.objects.get(pk=self.pk).img
                os.remove(old.path)
            except (Tournament.DoesNotExist, WindowsError):
                pass
            self.img.name = 'teams/' + self.slug + '.' + self.img.url.rsplit('.', 1)[1].lower()
        print(*args, **kwargs)
        super(Team, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('team-detail',
                       args=[self.slug])

    def get_delete_url(self):
        return reverse('team-delete',
                       args=[self.slug])


class Tournament(models.Model):
    class Status(models.TextChoices):
        OPENED = 'Open'
        CLOSED = 'Close'

    name = models.CharField(max_length=64)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    img = models.ImageField(upload_to='tournaments', blank=True)
    status = models.CharField(choices=Status.choices, default=Status.OPENED, max_length=16)

    game = models.ForeignKey('Game', related_name='tournament', on_delete=models.CASCADE)
    game_format = models.ForeignKey('GameFormat', related_name='tournament', on_delete=models.CASCADE)
    max_participants = models.IntegerField()
    participants = models.ManyToManyField('account.TournamentAccount', related_name='in_t', blank=True)
    likes = models.ManyToManyField('account.TournamentAccount', related_name='fav_t', blank=True)

    communication = models.CharField(max_length=64)
    contact = models.TextField(blank=True)

    contact_detail = models.TextField(blank=True)

    rules = models.TextField(blank=True)
    schedule = models.TextField(blank=True)
    prizes = models.TextField(blank=True)

    start_date = models.DateField()
    start_time = models.TimeField()
    end = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.img:
            try:
                old = Tournament.objects.get(pk=self.pk).img
                os.remove(old.path)
            except (Tournament.DoesNotExist, WindowsError):
                pass
            self.img.name = 'images/' + self.slug + '/' + 'main_image.' + self.img.url.rsplit('.', 1)[1].lower()
        super(Tournament, self).save(*args, **kwargs)


class GameFormat(models.Model):
    name = models.CharField(max_length=64)
    max_players = models.IntegerField()

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name
