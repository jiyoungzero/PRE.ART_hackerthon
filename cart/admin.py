from django.contrib import admin
from .models import Post

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('realname', 'artist_name', 'team', 'email', 'artist_intro', 'post_intro', 'post_plan', 'option')