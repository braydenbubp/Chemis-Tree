from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from chemappapi.models import Element
from chemappapi.views.element import ElementSerializer
import json
class ElementTests(APITestCase):
    def setUp(self):
        self.element_data = {
            "name": "element",
            "symbol": "E",
            "mass": 5.02,
            "group": "Non-Metal"
        }
    
    def test_create_element(self):
        url = "/elements"
        
        response = self.client.post(url, self.element_data, format='json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_element = Element.objects.last()
        expected = ElementSerializer(new_element)
        self.assertEqual(expected.data, response.data)
        
    def test_get_element(self):
        element = Element.objects.create(**self.element_data)
        
        url = f'/elements/{element.id}'
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = ElementSerializer(element)
        self.assertEqual(expected.data, response.data)
    
    def test_list_elements(self):
        self.test_create_element()
        self.test_create_element()
        self.test_create_element()
        
        url = "/elements"
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)
        
        self.assertEqual(len(response.data), Element.objects.count())

    def test_update_element(self):
        element = Element.objects.create(**self.element_data)
        url = f'/elements/{element.id}'

        updated_data = {
            "name": "new guy",
            "symbol": "Z",
            "mass": 5.69,
            "group": "Non-Metal"
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        element.refresh_from_db()
        
        expected_data = {
          'id': element.id,
          'name': updated_data['name'],
          'symbol': updated_data['symbol'],
          'mass': updated_data['mass'],
          'group': updated_data['group']
        }
        
        serializer = ElementSerializer(expected_data)
        self.assertEqual(serializer.data, response.data)
    
    def test_element_destroy(self):
        element = Element.objects.create(**self.element_data)
        element.refresh_from_db()
        self.assertTrue(Element.objects.filter(id=element.id).exists)

        url = f'/elements/{element.id}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        get_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, get_response.status_code)
