from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from chemappapi.models import Compound, Element, User, CompoundElement
import pubchempy as pcp

class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = ('id', 'user', 'user_id', 'iupac_name', 'molecular_formula', 'molecular_weight', 'cid', 'bonds', 'synonyms', 'elements')
        depth = 2
        
class CompoundView(ViewSet):
    
    def retrieve(self, request, pk):
        compound = Compound.objects.get(pk = compound.cid)

        serializer = CompoundSerializer(compound)
        return Response(serializer.data)
      
    def list(self, request):
        compounds = Compound.objects.all()
        serializer = CompoundSerializer(compounds)
        return Response(serializer.data, many=True)
    
    # not sure if i need this now, or need to do it in a different way  
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
      
    # to be fixed  
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

            
    
    @action(detail=False, methods=['post'], url_path='get_compound_by_element')
    def get_compound_by_element(self, request):
            include_elements = request.data["includeElements"]
            print(include_elements)

            compound_search = "".join(include_elements)
            print(compound_search)
            results = pcp.get_compounds(compound_search, "formula")
            print(results)
            
            if results:
                pubchem_compound = results[0]
                print(results[0].iupac_name)               
                user = User.objects.get(pk = request.data["user"])
                compound = Compound.objects.create(
                    user = user,
                    molecular_formula = pubchem_compound.molecular_formula,
                    iupac_name = pubchem_compound.iupac_name,
                    molecular_weight = pubchem_compound.molecular_weight,
                    cid = pubchem_compound.cid,
                    bonds = [{'aid1': bond.aid1, 'aid2': bond.aid2, 'order': bond.order} for bond in pubchem_compound.bonds],
                    synonyms = pubchem_compound.synonyms
                )
                
                serializer = CompoundSerializer(compound)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No compound found"}, status=status.HTTP_404_NOT_FOUND)
