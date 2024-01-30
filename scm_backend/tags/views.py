from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Tag, Keyword
from .serializers import *

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def tags(request):
    if request.method == 'GET':
        data = Tag.objects.all()

        serializer = TagSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        Tag.objects.all().delete()

        return Response(status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'DELETE'])
def tag(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
    except Tag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TagSerializer(tag, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TagSerializer(tag, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.
@api_view(['GET', 'DELETE'])
def keywords(request):
    if request.method == 'GET':
        data = Keyword.objects.all()

        serializer = KeywordSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    
    elif request.method == 'DELETE':
        Keyword.objects.all().delete()

        return Response(status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
def keyword(request, pk):
    try:
        keyword = Keyword.objects.get(pk=pk)
    except Keyword.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = KeywordSerializer(keyword, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = KeywordSerializer(keyword, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        keyword.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

