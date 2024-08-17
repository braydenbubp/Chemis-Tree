from chemspipy import ChemSpider

# cs = ChemSpider('rxSH6fXVGTFYU8GrTyJ6l6STu8MqXUh8')

# c = cs.get_compound(2157)

# print(c.molecular_formula)
# print(c.molecular_weight)
# print(c.smiles)
# print(c.common_name)

# for result in cs.search('C44H30N4Zn'):
#     print(result)


# creating a compound
# compound = cs.get_compound(2157)

# this instantiates the compound directly
# compound = Compound(cs, 2157)

# refs = cs.get_external_references(2157, datasources=['PubChem'])
# print(refs)

# info = cs.get_details(2157)
# print(info.keys())
# print(info['smiles'])

# print(cs.get_datasources())

# print(cs.convert('c1ccccc1', 'SMILES', 'InChI'))
# allowed conversions
# From InChI to InChIKey
# From InChI to Mol
# From InChI to SMILES
# From InChIKey to InChI
# From InChIKey to Mol
# From Mol to InChI
# From Mol to InChIKey
# From SMILES to InChI


# FE calls BE with request, BE querys 3rd party api, serializes, then sends to FE. 
# SQlite can still be used 
# below is how this might look


# models.py
# from django.db import models
# from django.contrib.auth.models import User

# class Compound(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=100)
#     formula = models.CharField(max_length=100)
#     data = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'name']

# # views.py
# from django.views import View
# from django.http import JsonResponse
# from django.contrib.auth.mixins import LoginRequiredMixin
# import requests
# from .models import Compound

# class CompoundView(LoginRequiredMixin, View):
#     def post(self, request):
#         # Create a new compound
#         name = request.POST.get('name')
#         formula = request.POST.get('formula')
        
#         # Query the 3rd party API for compound information
#         api_url = f'https://api.compounds.com/info/{formula}'
#         response = requests.get(api_url, headers={'Authorization': 'Bearer YOUR_API_KEY'})
        
#         if response.status_code == 200:
#             data = response.json()
#             compound = Compound.objects.create(
#                 user=request.user,
#                 name=name,
#                 formula=formula,
#                 data=data
#             )
#             return JsonResponse({'id': compound.id, 'name': name, 'formula': formula, 'data': data})
#         else:
#             return JsonResponse({'error': 'Failed to fetch compound data'}, status=400)

#     def get(self, request, compound_id=None):
#         if compound_id:
#             # Retrieve a specific compound
#             try:
#                 compound = Compound.objects.get(id=compound_id, user=request.user)
#                 return JsonResponse({
#                     'id': compound.id,
#                     'name': compound.name,
#                     'formula': compound.formula,
#                     'data': compound.data
#                 })
#             except Compound.DoesNotExist:
#                 return JsonResponse({'error': 'Compound not found'}, status=404)
#         else:
#             # List all compounds for the user
#             compounds = Compound.objects.filter(user=request.user).values('id', 'name', 'formula')
#             return JsonResponse(list(compounds), safe=False)

# # urls.py
# from django.urls import path
# from .views import CompoundView

# urlpatterns = [
#     path('api/compounds/', CompoundView.as_view(), name='compound_list'),
#     path('api/compounds/<int:compound_id>/', CompoundView.as_view(), name='compound_detail'),
# ]



# another example 


# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from django.views import View

# class CompoundView(View):
#     def get(self, request, compound_id):
#         return self.get_compound_details(compound_id)

#     def get_compound_details(self, record_id):
#         api_key = settings.CHEMSPIDER_API_KEY
#         api_url = 'https://api.rsc.org/v1/compounds'  # Adjust if needed
        
#         headers = {
#             'apikey': api_key,
#             'User-Agent': 'Your Application Name',  # Replace with your app name
#         }

#         fields = [
#             'SMILES', 'Formula', 'AverageMass', 'MolecularWeight', 'MonoisotopicMass',
#             'NominalMass', 'CommonName', 'ReferenceCount', 'DataSourceCount',
#             'PubMedCount', 'RSCCount', 'Mol2D', 'Mol3D'
#         ]

#         params = {
#             'fields': ','.join(fields),
#             'id': record_id
#         }

#         try:
#             response = requests.get(f'{api_url}/{record_id}/details', headers=headers, params=params)
#             response.raise_for_status()  # Raises an HTTPError for bad responses
            
#             data = response.json()
            
#             # Process the data as needed
#             processed_data = {
#                 'id': record_id,
#                 'name': data.get('CommonName', ''),
#                 'formula': data.get('Formula', ''),
#                 'smiles': data.get('SMILES', ''),
#                 'molecular_weight': data.get('MolecularWeight', ''),
#                 'average_mass': data.get('AverageMass', ''),
#                 # Add more fields as needed
#             }

#             return JsonResponse(processed_data)
        
#         except requests.RequestException as e:
#             return JsonResponse({'error': f'Failed to fetch compound data: {str(e)}'}, status=500)

# # In urls.py
# from django.urls import path
# from .views import CompoundView

# urlpatterns = [
#     path('api/compounds/<int:compound_id>/', CompoundView.as_view(), name='compound_detail'),
# ]


# possible post func for larger serach requests which is better than get requests

# import requests
# from django.conf import settings
# from django.http import JsonResponse
# from django.views import View

# class CompoundOperationView(View):
#     def post(self, request):
#         api_key = settings.CHEMSPIDER_API_KEY
#         api_url = 'https://api.rsc.org/v1'

#         headers = {
#             'apikey': api_key,
#             'Content-Type': 'application/json',
#             'User-Agent': 'Your Application Name',
#         }

#         # Extract parameters from the request
#         api = request.POST.get('api', 'compounds')
#         namespace = request.POST.get('namespace')
#         endpoint = request.POST.get('endpoint')
#         json_data = request.POST.get('json')

#         try:
#             response = requests.post(
#                 f'{api_url}/{api}/{namespace}/{endpoint}',
#                 headers=headers,
#                 json=json_data
#             )
#             response.raise_for_status()
            
#             return JsonResponse(response.json())
        
#         except requests.RequestException as e:
#             return JsonResponse({'error': f'API request failed: {str(e)}'}, status=500)

# # In urls.py
# from django.urls import path
# from .views import CompoundOperationView

# urlpatterns = [
#     path('api/compound-operation/', CompoundOperationView.as_view(), name='compound_operation'),
# ]


# model possibilities

# from django.db import models
# from django.contrib.auth.models import User

# class Compound(models.Model):
#     name = models.CharField(max_length=255)
#     formula = models.CharField(max_length=255)
#     smiles = models.TextField()
#     molecular_weight = models.FloatField(null=True, blank=True)
#     chemspider_id = models.IntegerField(unique=True)
#     last_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# class UserCompound(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     compound = models.ForeignKey(Compound, on_delete=models.CASCADE)
#     notes = models.TextField(blank=True)
#     favorite = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ['user', 'compound']

#     def __str__(self):
#         return f"{self.user.username} - {self.compound.name}"

# class Reaction(models.Model):
#     name = models.CharField(max_length=255)
#     reactants = models.ManyToManyField(Compound, related_name='reactions_as_reactant')
#     products = models.ManyToManyField(Compound, related_name='reactions_as_product')
#     description = models.TextField(blank=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name
