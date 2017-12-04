from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
  
  owner = serializers.ReadOnlyField(source='owner.username')
  
  class Meta:
    model = Tweet
    fields = ('id', 
              'content', 
              'owner', 
              'date_created', 
              'date_modified')
    read_only_fields = ('date_created', 'date_modified')