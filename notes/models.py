from django.db import models


class Notes(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
