# example of how it could look


# from django.db import models
# from django.contrib.auth.models import User

# class Compound(models.Model):
#     chemspider_id = models.IntegerField(unique=True)
#     name = models.CharField(max_length=255)
#     formula = models.CharField(max_length=255)
#     smiles = models.TextField()
#     molecular_weight = models.FloatField(null=True, blank=True)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
      
      

# from rest_framework import serializers
# from .models import Compound

# class CompoundSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Compound
#         fields = ('id', 'chemspider_id', 'name', 'formula', 'smiles', 'molecular_weight', 'last_updated')
        
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import status
# from django.conf import settings
# import requests

# class CompoundView(ViewSet):
#     def retrieve(self, request, pk=None):
#         try:
#             compound = Compound.objects.get(chemspider_id=pk)
#             if (timezone.now() - compound.last_updated).days > 7:  # Refresh data weekly
#                 self.update_compound_from_api(compound)
#         except Compound.DoesNotExist:
#             compound = self.fetch_and_create_compound(pk)
        
#         if compound:
#             serializer = CompoundSerializer(compound)
#             return Response(serializer.data)
#         else:
#             return Response({'message': 'Compound not found'}, status=status.HTTP_404_NOT_FOUND)

#     def list(self, request):
#         compounds = Compound.objects.all()
#         serializer = CompoundSerializer(compounds, many=True)
#         return Response(serializer.data)

#     def fetch_and_create_compound(self, chemspider_id):
#         api_data = self.fetch_from_chemspider_api(chemspider_id)
#         if api_data:
#             compound = Compound.objects.create(
#                 chemspider_id=chemspider_id,
#                 name=api_data.get('CommonName', ''),
#                 formula=api_data.get('Formula', ''),
#                 smiles=api_data.get('SMILES', ''),
#                 molecular_weight=api_data.get('MolecularWeight')
#             )
#             return compound
#         return None

#     def update_compound_from_api(self, compound):
#         api_data = self.fetch_from_chemspider_api(compound.chemspider_id)
#         if api_data:
#             compound.name = api_data.get('CommonName', compound.name)
#             compound.formula = api_data.get('Formula', compound.formula)
#             compound.smiles = api_data.get('SMILES', compound.smiles)
#             compound.molecular_weight = api_data.get('MolecularWeight', compound.molecular_weight)
#             compound.save()

#     def fetch_from_chemspider_api(self, chemspider_id):
#         api_key = settings.CHEMSPIDER_API_KEY
#         api_url = f'https://api.rsc.org/v1/compounds/{chemspider_id}/details'
        
#         headers = {
#             'apikey': api_key,
#             'Content-Type': 'application/json'
#         }
        
#         params = {
#             'fields': 'CommonName,Formula,SMILES,MolecularWeight'
#         }
        
#         try:
#             response = requests.get(api_url, headers=headers, params=params)
#             response.raise_for_status()
#             return response.json()
#         except requests.RequestException as e:
#             print(f"Error fetching data from ChemSpider: {e}")
#             return None
          


# from rest_framework.views import APIView

# class CompoundSearchView(APIView):
#     def post(self, request):
#         api_key = settings.CHEMSPIDER_API_KEY
#         api_url = 'https://api.rsc.org/v1/compounds/filter/substructure'
        
#         headers = {
#             'apikey': api_key,
#             'Content-Type': 'application/json'
#         }
        
#         # Assuming the request data contains the search parameters
#         search_params = request.data
        
#         try:
#             response = requests.post(api_url, headers=headers, json=search_params)
#             response.raise_for_status()
#             return Response(response.json())
#         except requests.RequestException as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# from django.urls import path
# from .views import CompoundView, CompoundSearchView

# urlpatterns = [
#     path('compounds/', CompoundView.as_view({'get': 'list'})),
#     path('compounds/<int:pk>/', CompoundView.as_view({'get': 'retrieve'})),
#     path('compounds/search/', CompoundSearchView.as_view()),
#     # ... your other url patterns ...
# ]


# --------------------------------------------------------------------------------------------


# possible setup for making compounds


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import requests
# from django.conf import settings

# class CompoundFromElementsView(APIView):
#     def post(self, request):
#         elements = request.data.get('elements', [])
#         if not elements:
#             return Response({'error': 'No elements provided'}, status=status.HTTP_400_BAD_REQUEST)

#         # Convert list of elements to a formula-like string
#         formula = ''.join(elements)

#         api_key = settings.CHEMSPIDER_API_KEY
#         api_url = 'https://api.rsc.org/v1/compounds/filter/formula'

#         headers = {
#             'apikey': api_key,
#             'Content-Type': 'application/json'
#         }

#         payload = {
#             'formula': formula,
#             'orderBy': 'Relevance',  # You can change this if needed
#             'orderDirection': 'Descending',
#             'limit': 10  # Limit to top 10 results
#         }

#         try:
#             response = requests.post(api_url, headers=headers, json=payload)
#             response.raise_for_status()
#             results = response.json()

#             # Now fetch details for each compound
#             compounds = []
#             for result in results.get('results', []):
#                 compound_details = self.fetch_compound_details(result['id'])
#                 if compound_details:
#                     compounds.append(compound_details)

#             return Response(compounds)
#         except requests.RequestException as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def fetch_compound_details(self, compound_id):
#         api_key = settings.CHEMSPIDER_API_KEY
#         api_url = f'https://api.rsc.org/v1/compounds/{compound_id}/details'

#         headers = {
#             'apikey': api_key,
#             'Content-Type': 'application/json'
#         }

#         params = {
#             'fields': 'CommonName,Formula,SMILES,MolecularWeight,InChI'
#         }

#         try:
#             response = requests.get(api_url, headers=headers, params=params)
#             response.raise_for_status()
#             return response.json()
#         except requests.RequestException:
#             return None


# from django.urls import path
# from .views import CompoundFromElementsView

# urlpatterns = [
#     # ... your other url patterns ...
#     path('compounds/from-elements/', CompoundFromElementsView.as_view()),
# ]
