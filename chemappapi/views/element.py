from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from chemappapi.models import Element

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'name', 'symbol', 'mass', 'group')
        
class ElementView(ViewSet):
    def retrieve(self, request, pk):
        try:
            element = Element.objects.get(pk=pk)
            serializer = ElementSerializer(element)
            return Response(serializer.data)
        except Element.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
      
    def list(self, request):
        elements = Element.objects.all()
        serializer = ElementSerializer(elements, many=True)
        return Response(serializer.data)
      
    # comment out after BE MVP   
    def create(self, request):
        element = Element.objects.create(
            name = request.data["name"],
            symbol = request.data["symbol"],
            mass = request.data["mass"],
            group = request.data["group"]
        )
        
        serializer = ElementSerializer(element)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # comment out after BE MVP
    def update(self, request, pk):
        element = Element.objects.get(pk=pk)
        element.name = request.data["name"]
        element.symbol = request.data["symbol"]
        element.mass = request.data["mass"]
        element.group = request.data["group"]
        
        element.save()
        serializer = ElementSerializer(element)
        return Response(serializer.data, status=status.HTTP_200_OK)
      
    # comment out after BE MVP  
    def destroy(self, request, pk):
        element = Element.objects.get(pk=pk)
        element.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
