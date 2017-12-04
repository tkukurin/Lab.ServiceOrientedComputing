from rest_framework import generics, permissions
from .permissions import IsOwner
from .serializers import TweetSerializer
from .models import Tweet

class CreateView(generics.ListCreateAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticated, IsOwner)
  
  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

    
class DetailsView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Tweet.objects.all()
  serializer_class = TweetSerializer
  permission_classes = (permissions.IsAuthenticated, IsOwner)

class UserTweetsView(generics.ListCreateAPIView):
    model = Tweet
    serializer_class = TweetSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id is not None:
            return Tweet.objects.filter(owner=user_id)
        return []
	