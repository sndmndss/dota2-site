from django.db import models
from social_django.models import UserSocialAuth


class SteamUser(models.Model):
    user_social_auth = models.OneToOneField(UserSocialAuth, on_delete=models.CASCADE,
                                            null=True, blank=True)
    steamID3 = models.CharField(max_length=15, primary_key=True)

    def __str__(self):
        return self.steamID3
