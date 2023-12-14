from django.db import models
from d2site.apps.home.models import SteamUser


class Comment(models.Model):
    steam_users = models.OneToOneField(SteamUser, on_delete=models.CASCADE)
    text = models.TextField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    match_id = models.CharField(max_length=30)  # TODO: посмотреть максимум
    author_uid = models.CharField(max_length=30)  # TODO: посмотреть максимум
    ratings = models.JSONField



