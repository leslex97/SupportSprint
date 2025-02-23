from django.db import models
from django.contrib.auth.models import User
from deskhelp.models import Department

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.user.username