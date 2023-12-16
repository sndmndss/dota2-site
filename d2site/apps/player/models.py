from django.db import models
from d2site.apps.home.models import SteamUser


class Comment(models.Model):
    steam_users = models.ForeignKey(SteamUser, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=200, blank=True)
    author_name = models.CharField(max_length=30, default="Unknown")
    author_uid = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    match_id = models.CharField(max_length=22)
    ratings = models.JSONField
    usefulness = models.IntegerField(default=0)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.text, self.author_name)



