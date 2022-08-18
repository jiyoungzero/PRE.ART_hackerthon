from typing import Reversible
from django.db import models
from atexit import register
from django.contrib.auth.models import User
from django.conf import settings


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=128)

    class Meta:
        permissions = (
            ("manager", "manager"),
            ("just_user", "just_user"),
        )    