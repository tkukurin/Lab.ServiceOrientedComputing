from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from .models import Bucketlist

class ModelTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username="toni")
    self.bucketlist_name = "X"
    self.bucketlist = Bucketlist(name=self.bucketlist_name, owner=user)
    
  def test_model_can_create_bucketlist(self):
    old_count = Bucketlist.objects.count()
    self.bucketlist.save()
    new_count = Bucketlist.objects.count()
    self.assertNotEqual(old_count, new_count)
    
    
class ViewTestCase(TestCase):
  def setUp(self):
    user = User.objects.create(username="toni")
    
    self.client = APIClient()
    self.client.force_authenticate(user=user)
    
    self.bucketlist_data = { 'name': 'finish this lab',
                           		'owner': user.id }
    self.response = self.client.post(
      reverse('create'), self.bucketlist_data, format='json')

  def test_api_can_create_bucketlist(self):
    self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
    
  def test_api_can_get_bucketlist(self):
    bucketlist = Bucketlist.objects.get()
    response = self.client.get(
    	reverse('details', kwargs={'pk': bucketlist.id}), format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
  
  def test_api_can_update_bucketlist(self):
    bucketlist = Bucketlist.objects.get()
    
    change_bucketlist = { 'name': 'New name' }
    result = self.client.put(
      reverse('details', kwargs={ 'pk': bucketlist.id }),
      change_bucketlist, format='json')
    
    self.assertEqual(result.status_code, status.HTTP_200_OK)
  
  def test_api_can_delete_bucketlist(self):
    bucketlist = Bucketlist.objects.get()
    
    response = self.client.delete(
      reverse('details', kwargs={ 'pk': bucketlist.id }),
      follow=True, format='json')
    
    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    