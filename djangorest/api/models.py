from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

class Tweet(models.Model):
  owner = models.ForeignKey(
    'auth.User', 
    on_delete=models.CASCADE)
  content = models.CharField(
    max_length=240, blank=False, unique=False)
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.content

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  if created:
    Token.objects.create(user=instance)