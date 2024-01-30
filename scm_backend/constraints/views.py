from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import ConstraintType, Constraint, ConstraintAssociation
from .serializers import ConstraintTypeSerializer, ConstraintSerializer, ConstraintAssociationSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def constraints(request):
    if request.method == 'GET':
        data = Constraint.objects.all()

        serializer = ConstraintSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConstraintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def constraint(request, pk):
    try:
        asset = Constraint.objects.get(pk=pk)
    except Constraint.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConstraintSerializer(asset, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ConstraintSerializer(asset, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def constraint_type(request):
    if request.method == 'GET':
        data = ConstraintType.objects.all()

        serializer = ConstraintTypeSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['GET', 'POST'])
def constraint_for_asset(request, pk):
    if request.method == 'GET':
        data = ConstraintAssociation.objects.filter(asset_id=pk)

        serializer = ConstraintAssociationSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ConstraintAssociationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def constraint_association(request, pk):
    try:
        constraint_association = ConstraintAssociation.objects.get(pk=pk)
    except ConstraintAssociation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ConstraintAssociationSerializer(constraint_association, context={'request': request})

        return Response(serializer.data)
    elif request.method == 'DELETE':
        constraint_association.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
