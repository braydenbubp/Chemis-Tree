from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from chemappapi.models import Compound, User, Tree, TreeCompound, Element
from chemappapi.views.tree import TreeSerializer
from chemappapi.views.compound import CompoundSerializer

class TreeTests(APITestCase):
    def setUp(self):
      
        self.user_data = {
          "name": "test",
          "uid": "testUid"
        }
        self.user = User.objects.create(**self.user_data)
        
        self.tree_data = {
          "name": "test",
          "uid": self.user
        }
        
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
        
        self.compound_data = {
            "user": self.user,
            "user_id": 1,
            "iupac_name": "methanone",
            "molecular_formula": "CHO+",
            "molecular_weight": 29.018,
            "cid": 6432172,
            "bonds": "[{'aid1': 1, 'aid2': 2, 'order': 2}, {'aid1': 2, 'aid2': 3, 'order': 1}]",
            "synonyms": "['Formyl cation', 'Oxomethylium', 'methylidyneoxidanium', '17030-74-9', 'carbon monoxide(1+)', 'Formylium', 'methylidyneoxonium', 'Methylium, oxo-', 'Formyl ion(1+)', 'Formyl(1+)']",
            # "elements": []
        }
    
    def test_create_tree(self):
        url = "/trees"
        
        response = self.client.post(url, {"name": self.tree_data["name"], "uid": self.user.uid}, format='json')
        
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        
        new_tree = Tree.objects.last()
        expected = TreeSerializer(new_tree)
        self.assertEqual(expected.data, response.data)
    
    def test_get_tree(self):
        tree = Tree.objects.create(name=self.tree_data['name'], uid=self.user)
        
        compound1 = Compound.objects.create(**self.compound_data)
        TreeCompound.objects.create(tree=tree, compound=compound1)
        # elements_data = Compound.objects.pop('elements')

        
        # for element in elements_data:
        #     element = Element.objects.get(**self.element_data)
        #     compound1.elements.add(element)
        
        url = f'/trees/{tree.id}'
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        
        expected = TreeSerializer(tree)
        self.assertEqual(expected.data, response.data)
        
    def test_list_trees(self):
        self.test_create_tree()
        self.test_create_tree()
        self.test_create_tree()
        
        url = "/trees"
        response = self.client.get(url)
        
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, list)
        
        self.assertEqual(len(response.data), Tree.objects.count())

    def test_update_tree(self):
        tree = Tree.objects.create(name=self.tree_data['name'], uid=self.user)
        url = f'/trees/{tree.id}'
        # user = User.objects.get(**self.user_data)
        
        compound1 = Compound.objects.create(**self.compound_data)
        TreeCompound.objects.create(tree=tree, compound=compound1)

        updated_data = {
            "name": "new_test",
            "uid": self.user.uid,
            "compounds": [compound1.id]
        }
        
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        tree.refresh_from_db()
        
        expected_data = Tree.objects.get(id=tree.id)
        
        serializer = TreeSerializer(expected_data)
        self.assertEqual(serializer.data, response.data)
        
    def test_destroy_tree(self):
        tree = Tree.objects.create(name=self.tree_data['name'], uid=self.user)
        tree.refresh_from_db()
        self.assertTrue(Tree.objects.filter(id=tree.id).exists)

        url = f'/trees/{tree.id}'
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        get_response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, get_response.status_code)
