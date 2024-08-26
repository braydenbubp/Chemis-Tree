from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chemappapi.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'uid')
        
class UserView(ViewSet):
    def retrieve(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
      
    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
      
    # comment out after BE MVP   
    def create(self, request):
        user = User.objects.create(
            name = request.data["name"],
            uid = request.data["uid"]
        )
        
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # comment out after BE MVP
    def update(self, request, pk):
        user = User.objects.get(id=pk)
        user.name = request.data["name"]
        user.uid = request.data["uid"]
        
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    # comment out after BE MVP  
    def destroy(self, request, pk):
        user = User.objects.get(id=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
