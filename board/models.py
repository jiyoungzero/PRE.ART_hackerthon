from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Board(models.Model):
    id = models.AutoField(primary_key=True)
    title       = models.CharField(max_length=200, null=True)
    contents    = models.TextField(blank=False,null=True)
    writer      = models.ForeignKey(User, on_delete=models.CASCADE)
    # 글쓴시간
    created_at  = models.DateTimeField(auto_now_add=True)
    # 글 수정한 시간
    updated_at  = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.title

    def summary(self):
        return self.contents[:10]

    class Meta:
        db_table            = 'boards'
        verbose_name        = 'board'
        verbose_name_plural = 'boards'

class Comment(models.Model):
   content = models.TextField()
   writer = models.ForeignKey(User, on_delete=models.CASCADE)
   board = models.ForeignKey( Board ,on_delete=models.CASCADE, related_name ='comments',null=True)
   created_at = models.DateTimeField(auto_now_add=True)
   update_at = models.DateTimeField(auto_now=True)
