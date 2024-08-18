from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chemappapi.models import Compound, Element, User, CompoundElement

class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = ('id', 'user', 'user_id', 'common_name', 'formula', 'smiles', 'molecular_weight', 'chemspider_id', 'two_d_model', 'elements')
        depth = 2
        
class CompoundView(ViewSet):
    def retrieve(self, request, pk):
        compound = Compound.objects.get(chemspider_id=pk)
        serializer = CompoundSerializer(compound)
        return Response(serializer.data)
      
    def list(self, request):
        compounds = Compound.objects.all()
        serializer = CompoundSerializer(compounds)
        return Response(serializer.data, many=True)
      
    def create(self, request):
        user = User.objects.get(uid=request.data["uid"])
        
        compound = Compound.objects.create(
            user = user,
            common_name = request.data["common_name"],
            formula = request.data["formula"],
            smiles = request.data["smiles"],
            molecular_weight = request.data["molecular_weight"],
            chemspider_id = request.data["chemspider_id"],
            two_d_model = request.data["two_d_model"],
        )
        
        for element_id in request.data["elements"]:
            element = Element.objects.get(pk=element_id)
            CompoundElement.objects.create(
                compound = compound,
                element = element
            )
        
        serializer = CompoundSerializer(compound)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        compound = Compound.objects.get(pk=pk)
                
        compound.common_name = request.data["common_name"],
        compound.formula = request.data["formula"],
        compound.smiles = request.data["smiles"],
        compound.molecular_weight = request.data["molecular_weight"],
        compound.chemspider_id = request.data["chemspider_id"],
        compound.two_d_model = request.data["two_d_model"],
        
        compound_elements = CompoundElement.objects.filter(compound_id = compound.id)
        for element in compound_elements:
            element.delete()
            
        compound.save()

        for element_id in request.data["elements"]:
            element = Element.objects.get(pk=element_id)
            CompoundElement.objects.create(
                compound = compound,
                element = element
            )
        
        serializer = CompoundSerializer(compound)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        compound = Compound.objects.get(pk=pk)
        compound.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
