from django.db import models
from django.contrib.auth.models import User
"""
class Message(models.Model):
    owner = models.ForeignKey(
      'auth.User', 
      on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
"""