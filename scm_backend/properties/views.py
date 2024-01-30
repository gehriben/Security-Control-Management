from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Property, PropertyTag
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def properties(request):
    if request.method == 'GET':
        data = Property.objects.all()

        serializer = PropertySerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        Property.objects.all().delete()

        return Response(status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'DELETE'])
def property(request, pk):
    try:
        property = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PropertySerializer(property, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PropertySerializer(property, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        property.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def property_tags(request):
    if request.method == 'DELETE':
        PropertyTag.objects.all().delete()

        return Response(status=status.HTTP_200_OK)
