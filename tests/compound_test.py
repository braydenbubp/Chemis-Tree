from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from chemappapi.models import Compound, User, Element
from chemappapi.views.compound import CompoundSerializer

class CompoundTests(APITestCase):
    def setUp(self):
        self.user_data = {
          "name": "test",
          "uid": "testUid"
        }
        self.user = User.objects.create(**self.user_data)
      
        self.element_data = [
              {
                  "id": 6,
                  "name": "Carbon",
                  "symbol": "C",
                  "mass": 12,
                  "group": "Nonmetal"
              },
              {
                  "id": 8,
                  "name": "Oxygen",
                  "symbol": "O",
                  "mass": 15,
                  "group": "Nonmetal"
              },
              {
                  "id": 1,
                  "name": "Hydrogen",
                  "symbol": "H",
                  "mass": 1,
                  "group": "Nonmetal"
              }
          ]
        for elements in self.element_data:
            Element.objects.create(**elements)

        self.compound_data = {
            "includeElements": ["C", "O"],
            "user": self.user.id,
            # "user_id": 1,
            # "iupac_name": "methanone",
            # "molecular_formula": "CHO+",
            # "molecular_weight": 29.018,
            # "cid": 6432172,
            # "bonds": "[{'aid1': 1, 'aid2': 2, 'order': 2}, {'aid1': 2, 'aid2': 3, 'order': 1}]",
            # "synonyms": "['Formyl cation', 'Oxomethylium', 'methylidyneoxidanium', '17030-74-9', 'carbon monoxide(1+)', 'Formylium', 'methylidyneoxonium', 'Methylium, oxo-', 'Formyl ion(1+)', 'Formyl(1+)']",
            # "elements": self.element_data
        }
        self.compound_for_get = {
            "user": self.user,
            "user_id": 1,
            "iupac_name": "methanone",
            "molecular_formula": "CHO+",
            "molecular_weight": 29.018,
            "cid": 6432172,
            "bonds": "[{'aid1': 1, 'aid2': 2, 'order': 2}, {'aid1': 2, 'aid2': 3, 'order': 1}]",
            "synonyms": "['Formyl cation', 'Oxomethylium', 'methylidyneoxidanium', '17030-74-9', 'carbon monoxide(1+)', 'Formylium', 'methylidyneoxonium', 'Methylium, oxo-', 'Formyl ion(1+)', 'Formyl(1+)']",
            # "elements": self.element_data
        }
        
    def create_compound(self, include_elements):
        url = "/compounds/get_compound_by_element"
        compound_data = self.compound_data.copy()
        compound_data['includeElements'] = include_elements
        response = self.client.post(url, compound_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        response_data = response.json()
        compound_id = response_data.get('id')
        
        return Compound.objects.get(id=compound_id)

    
    def test_create_compound(self):
        include_elements = ["H", "O"]
        compound = self.create_compound(include_elements)
        self.assertIsNotNone(compound.id)
        
        url = f'/compounds/{compound.id}'
        response = self.client.get(url)
        
        serializer = CompoundSerializer(compound)
        self.assertEqual(serializer.data, response.data)
        
    def test_get_compound(self):
        compound = Compound.objects.create(**self.compound_for_get)
        element_id = [element['id'] for element in self.element_data]
        compound.elements.set(Element.objects.filter(id__in = element_id))
        
        url = f'/compounds/{compound.id}'
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = CompoundSerializer(compound)
        self.assertEqual(expected.data, response.data)
        
    def test_list_compounds(self):
        self.create_compound(include_elements=["H", "O"])
        self.create_compound(include_elements=["H", "H", "O"])
        self.create_compound(include_elements=["H", "H", "O", "O"])
        
        url = "/compounds"
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), Compound.objects.count())
        
    def test_update_compound(self):
        compound = self.create_compound(include_elements=["H", "O"])
        url = f'/compounds/{compound.id}'
        # user = User.objects.get(**self.user_data)

        updated_data = {
          "includeElements": ["C", "O"],
          "user": self.user.id
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        compound.refresh_from_db()
        
        expected_data = Compound.objects.get(id=compound.id)
        
        serializer = CompoundSerializer(expected_data)
        self.assertEqual(serializer.data, response.data)

    def test_destroy_compound(self):
        compound = self.create_compound(include_elements=["H", "O"])
        compound.refresh_from_db()
        self.assertTrue(Compound.objects.filter(id=compound.id).exists)

        url = f'/compounds/{compound.id}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        get_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, get_response.status_code)
