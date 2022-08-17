from django.contrib import admin
from .models import Post, PostImage

# Register your models here.

# @admin.register(Post, PostAdmin)
class PhotoInline(admin.TabularInline):
    model = PostImage

class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]
    list_display = ('realname', 'artist_name', 'team', 'email', 'artist_intro', 'post_intro', 'post_plan', 'option')

admin.site.register(Post, PostAdmin)