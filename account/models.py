from django.db import models
from django.conf import settings
from django.urls import reverse


class TournamentAccount(models.Model):
    class Actions(models.TextChoices):
        FILL_REGISTER_FORM = 'register'
        FILL_TOURNAMENT_FORM = 'register_tournament'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True, default=None)
    action = models.CharField(choices=Actions.choices, max_length=32, default=None, null=True)

    def save(self, *args, **kwargs):
        if self.photo:
            self.photo.name = self.user.username + '/' + 'avatar.' + self.photo.url.rsplit('.', 1)[1].lower()
        super(TournamentAccount, self).save()


class ActivateToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
                                related_name='activation_token')
    token = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse('register_activate', args=[self.token])
