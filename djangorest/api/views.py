from rest_framework import generics, permissions, views
from rest_framework.response import Response

from .permissions import IsOwner, IsOwnerOrReadOnly
from .serializers import TweetSerializer, UserSerializer
from .models import Tweet

from django.contrib.auth.models import User


class TweetCreateView(generics.ListCreateAPIView):
  """
	get:
	List all Tweets. Authentication is not necessary for this endpoint.
	
	post:
	Create new Tweet for authenticated user.
  """
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class TweetDetailsView(generics.RetrieveUpdateDestroyAPIView):
  """
	get:
	Get Tweet with given ID. Authentication is not necessary for this endpoint.
	
	put:
	Update Tweet with given ID. Authenticated user must be the owner of the Tweet.
	
	patch:
	Update Tweet with given ID. Authenticated user must be the owner of the Tweet.
	
	delete:
	Delete Tweet with given ID. Authenticated user must be the owner of the Tweet.
  """
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

class UserCreateView(generics.ListCreateAPIView):
  """
	get:
	List all users. Authentication is not necessary for this endpoint.
	
	post:
	Create new user. Authentication is not necessary for this endpoint.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer
	
class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	
class UserTweetsView(generics.RetrieveAPIView):
  """
  List all Tweets for user with given ID. Authentication is not necessary for this endpoint.
  """
  def get(self, request, user_id, format=None):
    tweets = TweetSerializer(data=Tweet.objects.filter(owner_id=user_id), many=True)
    tweets.is_valid()
    return Response(tweets.data)