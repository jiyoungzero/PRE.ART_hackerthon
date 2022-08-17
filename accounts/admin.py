from django.contrib import admin
from .models import Member
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.

class MemberAdmin(admin.StackedInline):
    model = Member
    con_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (MemberAdmin,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)