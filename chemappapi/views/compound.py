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
        compound = Compound.objects.get(pk = pk)

        serializer = CompoundSerializer(compound)
        return Response(serializer.data)
      
    def list(self, request):
        compounds = Compound.objects.all()
        serializer = CompoundSerializer(compounds, many=True)
        return Response(serializer.data)
      
    # to be fixed  
    def update(self, request, pk):
        try:
            compound = Compound.objects.get(pk=pk)
            user = request.data.get("user")
            include_elements = request.data.get("includeElements", [])
            
            compound_search = "".join(include_elements)
            results = pcp.get_compounds(compound_search, "formula")


            if results:
                pubchem_compound = results[0]
                # print("PubChem data:", {
                #     "molecular_formula": pubchem_compound.molecular_formula,
                #     "iupac_name": pubchem_compound.iupac_name,
                #     "molecular_weight": pubchem_compound.molecular_weight,
                #     "cid": pubchem_compound.cid,
                #     "bonds": pubchem_compound.bonds,
                #     "synonyms": pubchem_compound.synonyms
                # })

                compound.molecular_formula = pubchem_compound.molecular_formula
                compound.iupac_name = pubchem_compound.iupac_name or "None"
                compound.molecular_weight = pubchem_compound.molecular_weight
                compound.cid = pubchem_compound.cid
                compound.bonds = [{'aid1': bond.aid1, 'aid2': bond.aid2, 'order': bond.order} for bond in pubchem_compound.bonds]
                compound.synonyms = pubchem_compound.synonyms[:10] if pubchem_compound.synonyms else []
                
                compound_elements = CompoundElement.objects.filter(compound_id = compound.id)
                for element in compound_elements:
                    element.delete()
                
                compound.save()
                
                for element_symbol in request.data["includeElements"]:
                    try:
                        element = Element.objects.get(symbol = element_symbol)
                        CompoundElement.objects.create(
                            compound = compound,
                            element = element
                        )
                    except Element.DoesNotExist:
                        print(f"element {element_symbol} DNE")
                        
                serializer = CompoundSerializer(compound)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("compound DNE", status=status.HTTP_404_NOT_FOUND)

        except Compound.DoesNotExist:
            return Response("compound DNE", status=status.HTTP_404_NOT_FOUND)
                

      
    def destroy(self, request, pk):
        compound = Compound.objects.get(pk=pk)
        compound.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)

            
    
    @action(detail=False, methods=['post'], url_path='get_compound_by_element')
    def get_compound_by_element(self, request):
            include_elements = request.data["includeElements"]

            compound_search = "".join(include_elements)
            results = pcp.get_compounds(compound_search, "formula")
            
            if results:
                pubchem_compound = results[0]
                user = User.objects.get(pk = request.data["user"])
                compound = Compound.objects.create(
                    user = user,
                    molecular_formula = pubchem_compound.molecular_formula,
                    iupac_name = pubchem_compound.iupac_name,
                    molecular_weight = pubchem_compound.molecular_weight,
                    cid = pubchem_compound.cid,
                    bonds = [{'aid1': bond.aid1, 'aid2': bond.aid2, 'order': bond.order} for bond in pubchem_compound.bonds],
                    synonyms = pubchem_compound.synonyms[:10] if pubchem_compound.synonyms else [],
                )
                
                for element_symbol in request.data["includeElements"]:
                    try:
                        element = Element.objects.get(symbol = element_symbol)
                        CompoundElement.objects.create(
                            compound = compound,
                            element = element
                        )
                    except Element.DoesNotExist:
                        print(f"element {element_symbol} DNE")
                
                serializer = CompoundSerializer(compound)
                
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "No compound found"}, status=status.HTTP_404_NOT_FOUND)


            
