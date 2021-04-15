from django.db import models
from django.conf import settings
from django.urls import reverse
import os


class TournamentAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='account', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True, default=None)

    def save(self, *args, **kwargs):

        if self.photo:
            try:
                old = TournamentAccount.objects.get(pk=self.pk).img
                os.remove(old.path)
            except (TournamentAccount.DoesNotExist, WindowsError):
                pass
            self.photo.name = self.user.username + '/' + 'avatar.' + self.photo.url.rsplit('.', 1)[1].lower()
        super(TournamentAccount, self).save()


class ActivateToken(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE,
                                related_name='activation_token')
    token = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse('register_activate', args=[self.token])
