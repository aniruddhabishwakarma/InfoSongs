from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_google_user = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
    profile_picture = models.URLField(blank=True, null=True)
    given_name = models.CharField(max_length=100, blank=True, null=True)
    family_name = models.CharField(max_length=100, blank=True, null=True)
    locale = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username