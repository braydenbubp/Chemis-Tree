from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from chemappapi.models import User
from chemappapi.views.user import UserSerializer
import sys

class UserTests(APITestCase):
    fixtures = ['users']
    def setUp(self):
        self.user_data = {
          "name": "test",
          "uid": "testUid"
        }
    
    def test_create_user(self):
        url = "/users"
        
        user = {
          "name": "brayden",
          "uid": "cvnjidfsnjb7575"
        }
        
        response = self.client.post(url, user, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_user = User.objects.last()
        expected = UserSerializer(new_user)
        self.assertEqual(expected.data, response.data)
        
        return new_user.id
      
    def test_get_user(self):
        user = User.objects.create(**self.user_data)
        
        url = f'/users/{user.id}'
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = UserSerializer(user)
        self.assertEqual(expected.data, response.data)
        
    def test_list_user(self):
        self.test_create_user()
        self.test_create_user()
        self.test_create_user()
        
        url = "/users"
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)
        
        self.assertEqual(len(response.data), User.objects.count())
        
    def test_update_user(self):
        user = User.objects.create(**self.user_data)
        url = f'/users/{user.id}'

        updated_data = {
          "name": "new user",
          "uid": "new uid"
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user.refresh_from_db()
        
        expected_data = {
          'id': user.id,
          'name': updated_data['name'],
          'uid': updated_data['uid']
        }
        
        serializer = UserSerializer(expected_data)
        self.assertEqual(serializer.data, response.data)
        
    def test_destroy_user(self):
        user = User.objects.create(**self.user_data)
        user.refresh_from_db()
        self.assertTrue(User.objects.filter(id=user.id).exists)

        url = f'/users/{user.id}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        get_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, get_response.status_code)
