from rest_framework import generics, permissions, views
from rest_framework.response import Response

from .permissions import IsOwner, IsOwnerOrReadOnly
from .serializers import TweetSerializer, UserSerializer
from .models import Tweet

from django.contrib.auth.models import User


class TweetCreateView(generics.ListCreateAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class TweetDetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class UserCreateView(generics.ListCreateAPIView):
  """
	get:
	Retrieves user data.
	
	post:
	Creates new user.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
	
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	
class UserTweetsView(generics.RetrieveAPIView):
  """
  Retrieves all Tweets for given user.
  """
	
  def get(self, request, user_id, format=None):
    tweets = TweetSerializer(data=Tweet.objects.filter(owner_id=user_id), many=True)
    tweets.is_valid()
    return Response(tweets.data)