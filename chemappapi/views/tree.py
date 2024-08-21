from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chemappapi.models import Tree, User

class TreeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'uid')

class TreeView(ViewSet):
    def retrieve(self, request, pk):
        tree = Tree.objects.get(pk=pk)
        serializer = TreeSerializer(tree)
        return Response(serializer.data)
      
    def list(self, request):
        trees = Tree.objects.all()
        serializer = TreeSerializer(trees, many=True)
        return Response(serializer.data)
      
    def create(self, request):
        user = User.objects.get(uid=request.data["uid"])
        
        tree = Tree.objects.create(
          user = user,
          name = request.data["name"]
        )
        
        serializer = TreeSerializer(tree)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      
    def update(self, request, pk):
        tree = Tree.objects.get(pk=pk)
        
        tree.name = request.data["name"]
        tree.save()
        serializer = TreeSerializer(tree)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    def destroy(self, request, pk):
        tree = Tree.objects.get(pk=pk)
        tree.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
      
# action method for adding compounds to trees or for loop similar to tags? 
# likely action method so that you create the compound add its attached to the tree id?
# potential action method for compounds not trees to accomlpish this?
