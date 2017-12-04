from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Tweet

class ModelTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username="toni")
    self.tweet_contents = "This is a test tweet."
    self.tweet = Tweet(content=self.tweet_contents, owner=user)
    
  def test_model_can_create_tweet(self):
    old_count = Tweet.objects.count()
    self.tweet.save()
    new_count = Tweet.objects.count()
    self.assertNotEqual(old_count, new_count)
    
    
class ViewTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username="toni")
    
    self.client = APIClient()
    self.client.force_authenticate(user=user)
    
    self.tweet_data = { 'content': 'Tweet content', 'owner': user.id }
    self.response = self.client.post(
      reverse('create'), self.tweet_data, format='json')

  def test_api_can_create_tweet(self):
    self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    
  def test_api_can_get_tweet(self):
    tweet = Tweet.objects.get()
    response = self.client.get(
    	reverse('details', kwargs={'pk': tweet.id}), format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
  
  def test_api_can_update_tweet(self):
    tweet = Tweet.objects.get()
    
    change_tweet = { 'content': 'New Tweet contents' }
    result = self.client.put(
      reverse('details', kwargs={ 'pk': tweet.id }),
      change_tweet, format='json')
    
    self.assertEqual(result.status_code, status.HTTP_200_OK)
  
  def test_api_can_delete_tweet(self):
    tweet = Tweet.objects.get()
    
    response = self.client.delete(
      reverse('details', kwargs={ 'pk': tweet.id }),
      follow=True, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    