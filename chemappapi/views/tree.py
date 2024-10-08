from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chemappapi.models import Tree, User, Compound, TreeCompound
from .compound import CompoundSerializer

class TreeSerializer(serializers.ModelSerializer):
    compounds = serializers.SerializerMethodField()
    def get_compounds(self, object):
        compound = Compound.objects.filter(trees__tree_id=object)
        serializer = CompoundSerializer(compound, many=True)
        return serializer.data
    class Meta:
        model = Tree
        fields = ('id', 'name', 'uid', 'compounds')
        depth = 1

class TreeView(ViewSet):
    def retrieve(self, request, pk):
        try:
            tree = Tree.objects.get(pk=pk)
            serializer = TreeSerializer(tree)
            return Response(serializer.data)
        except Tree.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def list(self, request):
        try:
            uid = request.query_params.get('uid', None)
            if uid is not None:
                user_id = User.objects.get(uid=uid)
                trees = Tree.objects.filter(uid = user_id)

            serializer = TreeSerializer(trees, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"message": "An error occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      
    def create(self, request):
        uid = User.objects.get(uid=request.data["uid"])
        
        tree = Tree.objects.create(
          uid = uid,
          name = request.data["name"]
        )
        
        for compound_id in request.data.get("compounds", []):
            compound = Compound.objects.get(pk=compound_id)
            TreeCompound.objects.create(
                compound = compound,
                tree = tree
            ) 
        
        serializer = TreeSerializer(tree)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        tree = Tree.objects.get(pk=pk)
        
        tree.name = request.data["name"]
        
        tree_compounds = TreeCompound.objects.filter(tree_id=tree.id)
        for compounds in tree_compounds:
            compounds.delete()
            
        tree.save()
        
        for compound_id in request.data.get("compounds", []):
            compound = Compound.objects.get(pk=compound_id)
            TreeCompound.objects.create(
                compound = compound,
                tree = tree
            ) 

        serializer = TreeSerializer(tree)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        tree = Tree.objects.get(pk=pk)
        tree.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
