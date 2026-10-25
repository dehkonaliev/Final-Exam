from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
import secrets


def default_expiry():
    return timezone.now() + timedelta(minutes=15)

class TempUser(models.Model):
    email = models.EmailField(max_length=100)
    code = models.IntegerField(blank=True, null=True)
    expiry_time = models.DateTimeField(default=default_expiry)
    
def generate_token():
    return secrets.token_urlsafe(32)
    
class MyToken(models.Model):
    temp_user = models.ForeignKey(TempUser, on_delete=models.CASCADE, related_name='my_tokens')
    token = models.CharField(max_length=64, default=generate_token)