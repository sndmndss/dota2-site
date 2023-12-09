from django.db import models
from django.conf import settings
from django.utils import timezone


class Match(models.Model):
    match_id = models.BigIntegerField(unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    match_data = models.JSONField()
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Match {self.match_id}"
