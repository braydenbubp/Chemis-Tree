from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from chemappapi.models import Compound, Element, User, CompoundElement
from chemapp.settings import CHEMSPIDER_API_KEY
from chemspipy import ChemSpider
from chemspipy.objects import Compound as Chem_Compound

class CompoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compound
        fields = ('id', 'user', 'user_id', 'common_name', 'formula', 'smiles', 'molecular_weight', 'chemspider_id', 'two_d_model', 'elements')
        depth = 2
        
cs = ChemSpider(CHEMSPIDER_API_KEY)
class CompoundView(ViewSet):
    
    def retrieve(self, request, pk):
        print(request.data)
        compound = cs.filter_element(self, include_elements, exclude_elements=None, include_all=False)
        print(compound)
        
        
        # compound = Compound.objects.get(chemspider_id=pk)
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
    
            
    # this works but returns the queryId and not the bject    
    # after fixing queryId being the response, an error for compond not existing arises due to syntax
    # i.e H{2}O{2} instead of H2O2 which is needed for the api 
    @action(detail=False, methods=['post'], url_path='get_compound_by_element')
    def get_compound_by_element(self, request):
            include_elements = request.data["includeElements"]

            element_symbols = []
            for element in include_elements:
                search_result = cs.search(element)
                element_symbols.append(search_result[0].molecular_formula)

            print(f'element_symbols', element_symbols)
            formula = ''.join(element_symbols)
            try:
                response = cs.filter_formula(formula)
                if 'queryId' in response:
                    compound_data = cs.filter_results(response['queryId'])
                    return Response({
                        'csid': compound_data.csid,
                        'molecular_formula': compound_data.molecular_formula,
                        'molecular_weight': compound_data.molecular_weight,
                        'iupac_name': compound_data.iupac_name,
                        'smiles': compound_data.smiles,
                        'inchi': compound_data.inchi,
                        'inchikey': compound_data.inchikey,
                    })
                else:
                    return Response({"error": f"No compound found for formula: {formula}"}, status=404)
            except Exception as e:
                print(f"Error retrieving compound: {e}")
                return Response({"error": str(e)}, status=400)
