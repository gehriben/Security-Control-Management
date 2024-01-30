from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Control
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def controls(request):
    if request.method == 'GET':
        data = Control.objects.all()

        serializer = ControlSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ControlSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE':
        Control.objects.all().delete()

        return Response(status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'DELETE'])
def control(request, pk):
    try:
        control = Control.objects.get(pk=pk)
    except Control.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ControlSerializer(control, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ControlSerializer(control, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        control.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def parent_controls(request):
    if request.method == 'GET':
        data = Control.objects.filter(parent_control=None)

        serializer = ControlSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET'])
def child_controls(request, parent_pk):
    try:
        parent_control = Control.objects.get(pk=parent_pk)
    except Control.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = Control.objects.filter(parent_control=parent_control)

        serializer = ControlSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
