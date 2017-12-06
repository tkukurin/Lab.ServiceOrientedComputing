from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Tweet


class TweetTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create(username="toni", password="mypassword")
    self.tweet = Tweet.objects.create(owner=self.user, content="johnny greenwood")
    
    self.user2 = User.objects.create(username="not_toni", password="mypassword")
    self.tweet2 = Tweet.objects.create(owner=self.user2, content="thom yorke")
  
  def test_tweet_get(self):
    client = APIClient()
    response = client.get('/api/v1/tweets/{0}/'.format(self.tweet.id))
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['content'], 'johnny greenwood')
  
  def test_tweet_list(self):
    client = APIClient()
    response = client.get('/api/v1/tweets/')
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json()), 2)
    self.assertEqual(response.json()[0]['content'], 'johnny greenwood')
    self.assertEqual(response.json()[1]['content'], 'thom yorke')
  
  def test_tweet_list_for_user(self):
    client = APIClient()
    response = client.get('/api/v1/users/{0}/tweets/'.format(self.user.id))
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(len(response.json()), 1)
    self.assertEqual(response.json()[0]['content'], 'johnny greenwood')
    
  def test_tweet_create(self):
    old_count = Tweet.objects.count()
    
    client = APIClient()
    client.force_authenticate(self.user)
    response = client.post('/api/v1/tweets/', {'content': 'johnny greenwood'})
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(Tweet.objects.count(), old_count + 1)
    
  def test_tweet_create_unauthenticated(self):
    old_count = Tweet.objects.count()
    
    client = APIClient()
    response = client.post('/api/v1/tweets/', {'content': 'johnny greenwood'})
    
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Tweet.objects.count(), old_count)
    
  def test_tweet_update(self):   
    client = APIClient()
    client.force_authenticate(self.user)
    response = client.post('/api/v1/tweets/', {'content': 'johnny greenwood'})
    id = response.json()['id']
    
    old_count = Tweet.objects.count()
    response = client.put('/api/v1/tweets/{0}/'.format(id), 
                          {'content': 'johnny greenwood 2'})
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Tweet.objects.count(), old_count)
    self.assertEqual(
      Tweet.objects.get(pk=id).content,
      'johnny greenwood 2')
    
  def test_tweet_update_unauthenticated(self):
    client = APIClient()
    client.force_authenticate(self.user)
    response = client.post('/api/v1/tweets/', {'content': 'johnny greenwood'})
    id = response.json()['id']
    
    client.force_authenticate(self.user2)
    response = client.put('/api/v1/tweets/{0}/'.format(id), 
                          {'content': 'johnny greenwood 2'})
    
    self.assertEqual(response.status_code, 403)
    self.assertEqual(
      Tweet.objects.get(pk=id).content,
      'johnny greenwood')
    
  def test_tweet_delete(self):
    client = APIClient()
    client.force_authenticate(self.user)
    response = client.post('/api/v1/tweets/', {'content': 'johnny greenwood'})
    old_count = Tweet.objects.count()
    
    response = client.delete('/api/v1/tweets/{0}/'.format(response.json()['id']))
    
    self.assertEqual(response.status_code, 204)
    self.assertEqual(Tweet.objects.count(), old_count - 1)
    
  def test_tweet_delete_unauthenticated(self):
    client = APIClient()
    client.force_authenticate(self.user)
    response = client.post('/api/v1/tweets/', {'content': 'johnny greenwood'})
    count = Tweet.objects.count()
    
    client.force_authenticate(self.user2)
    response = client.delete('/api/v1/tweets/{0}/'.format(response.json()['id']))
    
    self.assertEqual(response.status_code, 403)
    self.assertEqual(Tweet.objects.count(), count)

class UserTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create(username="toni", password="mypassword", email="myemail")
    self.user2 = User.objects.create(username="not_toni", password="mypassword", email="myotheremail")

  def test_user_get(self):
    client = APIClient()
    response = client.get('/api/v1/users/{0}/'.format(self.user.id))
    
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()['username'], 'toni')
    self.assertEqual(response.json()['email'], 'myemail')
    self.assertEqual(response.json().get('password', None), None)
    
  def test_user_create(self):
    old_count = User.objects.count()
    
    client = APIClient()
    response = client.post('/api/v1/users/', {'username': 'john', 'password': 'smith'})
    
    self.assertEqual(response.status_code, 201)
    self.assertEqual(User.objects.count(), old_count + 1)
    
  def test_user_update(self):
    client = APIClient()
    client.force_authenticate(self.user)
    
    old_password = User.objects.get(pk=self.user.id).password
    response = client.put('/api/v1/users/{0}/'.format(self.user.id),
                          {'username': 'johnny', 'password': 'smith'})
    
    self.assertEqual(response.status_code, 200)
    self.assertNotEqual(
      User.objects.get(pk=self.user.id).password,
      old_password)
    self.assertEqual(
      User.objects.get(pk=self.user.id).username,
      'johnny')
    
  def test_user_update_unauthenticated(self):
    client = APIClient()
    
    client.force_authenticate(self.user2)
    response = client.put('/api/v1/users/{0}/'.format(self.user.id),
                          {'username': 'john', 'password': 'smith'})
    
    self.assertEqual(response.status_code, 403)
    self.assertEqual(
      User.objects.get(pk=self.user.id).username,
      self.user.username)
    
  def test_user_delete(self):
    old_count = User.objects.count()
    
    client = APIClient()
    client.force_authenticate(self.user)
    response = client.delete('/api/v1/users/{0}/'.format(self.user.id))
    
    self.assertEqual(response.status_code, 204)
    self.assertEqual(User.objects.count(), old_count - 1)
    
  def test_user_delete_unauthenticated(self):
    old_count = User.objects.count()
    
    client = APIClient()
    client.force_authenticate(self.user2)
    response = client.delete('/api/v1/users/{0}/'.format(self.user.id))
    
    self.assertEqual(response.status_code, 403)
    self.assertEqual(User.objects.count(), old_count)
    