from django.db import models
from d2site.apps.home.models import SteamUser


class Comment(models.Model):
    steam_users = models.ForeignKey(SteamUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    match_id = models.CharField(max_length=30, default=0)  # TODO: посмотреть максимум
    author_uid = models.CharField(max_length=30)  # TODO: посмотреть максимум
    ratings = models.JSONField(default={"smurf": 0})
    author_name = models.CharField(max_length=20, default='Unknown')
    usefulness = models.IntegerField(default=0)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author_name)
