from django.db import models
from django.conf import settings
from slugify import slugify


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
        super(Team, self).save(*args, **kwargs)


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
    contact_detail = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    schedule = models.TextField(blank=True)
    prizes = models.TextField(blank=True)

    start_date = models.DateField()
    start_time = models.TimeField()
    end = models.DateTimeField(blank=True)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if self.img:
            self.img.name = 'images/' + self.slug + '/' + 'main_image' + self.img.url.rsplit('.', 1)[1].lower()
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
