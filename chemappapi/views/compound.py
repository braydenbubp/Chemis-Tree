import json
import traceback
from rdkit import Chem
from rdkit.Chem import Draw
from django.http import HttpResponseServerError
from django.db import transaction
from django.conf import settings
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from chemappapi.models import Compound, Element, User, CompoundElement
import pubchempy as pcp
from io import BytesIO
from django.core.files.base import ContentFile

class CompoundSerializer(serializers.ModelSerializer):
    model_2d_url = serializers.SerializerMethodField()
    class Meta:
        model = Compound
        fields = ('id', 'user', 'user_id', 'iupac_name', 'molecular_formula', 'molecular_weight', 'cid', 'bonds', 'synonyms', 'elements', 'model_2d', 'model_2d_url')
        depth = 2
        
    def get_model_2d_url(self, obj):
        if obj.model_2d:
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(obj.model_2d.url)
            return f"{settings.MEDIA_URL}{obj.model_2d.name}"
        return None
        
class CompoundView(ViewSet):
    
    def retrieve(self, request, pk):
        try:
            compound = Compound.objects.get(pk = pk)

            serializer = CompoundSerializer(compound)
            return Response(serializer.data)
        except Compound.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def list(self, request):
        try:
            user = request.query_params.get('uid', None)
            if user is not None:
                user_id = User.objects.get(uid=user)
                compounds = Compound.objects.filter(user = user_id)

            serializer = CompoundSerializer(compounds, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "An error occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
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
            user_uid = request.data["user"]
            user = User.objects.get(uid=user_uid)
            
            if not include_elements or not user_uid:
                return Response({"message": "Missing required data"}, status=status.HTTP_404_NOT_FOUND)

            compound_search = "".join(include_elements)
            results = pcp.get_compounds(compound_search, "formula")
            
            if not results:
                return Response({"message": "Compound not found"}, status=status.HTTP_404_NOT_FOUND)
            
            pubchem_compound = results[0]
            
            existing_compound_check = Compound.objects.filter(
                user = user,
                cid = pubchem_compound.cid
            ).first()
            
            if existing_compound_check:
                serializer = CompoundSerializer(existing_compound_check)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            try:
                with transaction.atomic():
                    compound = Compound.objects.create(
                        user = user,
                        molecular_formula = pubchem_compound.molecular_formula,
                        iupac_name = pubchem_compound.iupac_name or "Not Available",
                        molecular_weight = pubchem_compound.molecular_weight,
                        cid = pubchem_compound.cid,
                        bonds = json.dumps([{'aid1': bond.aid1, 'aid2': bond.aid2, 'order': bond.order} for bond in pubchem_compound.bonds]),
                        synonyms = json.dumps(pubchem_compound.synonyms[:10] if pubchem_compound.synonyms else []),
                    )
                    
                    mol = Chem.MolFromSmiles(pubchem_compound.isomeric_smiles)
                    img = Draw.MolToImage(mol)
                    
                    img_io = BytesIO()
                    img.save(img_io, format='PNG')
                    img_content = ContentFile(img_io.getvalue())
                    compound.model_2d.save(f"{compound.cid}_2d.png", img_content)
                    
                    for element_symbol in request.data["includeElements"]:
                        try:
                            element = Element.objects.get(symbol = element_symbol)
                            CompoundElement.objects.create(
                                compound = compound,
                                element = element
                            )
                        except Element.DoesNotExist:
                            print(f"element {element_symbol} DNE")
                    
                    try:
                        serializer = CompoundSerializer(compound, context={'request': request})
                        print(serializer.data['model_2d_url'])
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    except Exception as e:
                        print(f'error: {str(e)}')
                        print(f"traceback: {traceback.format_exc()}")
                        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except ValueError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": "An error occured while querying the database"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
