from rest_framework import generics, permissions, views, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .permissions import IsOwner, IsOwnerOrReadOnly
from .serializers import TweetSerializer, UserSerializer
from .models import Tweet

from django.contrib.auth.models import User


class CreateView(generics.ListCreateAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class TweetCreate(generics.ListCreateAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticated, )
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class UserDetails(generics.ListCreateAPIView):
  """
	get:
	Retrieves user data.
	
	post:
	Creates new user.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

	
class UserTweetsView(generics.RetrieveAPIView):
  """
  Retrieves all Tweets for given user.
  """
	
  def get(self, request, user_id, format=None):
    tweets = TweetSerializer(data=Tweet.objects.filter(owner_id=user_id), many=True)
    tweets.is_valid()
    return Response(tweets.data)