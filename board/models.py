from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Board(models.Model):
    title       = models.CharField(max_length=200)
    contents    = models.TextField()
    writer      = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def summary(self):
        return self.contents[:10]

    class Meta:
        db_table            = 'boards'
        verbose_name        = 'board'
        verbose_name_plural = 'boards'