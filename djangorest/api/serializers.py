from rest_framework import serializers
from .models import Tweet
from django.contrib.auth.models import User

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
    
class UserSerializer(serializers.ModelSerializer):
  
  class Meta:
      model = User
      fields = ('id', 'username', 'password', 'email')
      extra_kwargs = {
          'password': {'write_only': True},
      }

  def create(self, validated_data):
      user = User.objects.create_user(**validated_data)
      return user

  def update(self, instance, validated_data):
      if 'password' in validated_data:
          password = validated_data.pop('password')
          instance.set_password(password)
      return super(UserSerializer, self).update(instance, validated_data)