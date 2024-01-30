import traceback

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Asset, Assettype, AssetControlMatch
from .serializers import *
from .file_import import FileImport
from metrics.metrics import Metrics

# Create your views here.
@api_view(['GET', 'POST', 'DELETE'])
def assets(request):
    if request.method == 'GET':
        data = Asset.objects.all()

        serializer = AssetSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AssetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        Asset.objects.all().delete()

        return Response(status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'DELETE'])
def asset(request, pk):
    try:
        asset = Asset.objects.get(pk=pk)
    except Asset.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AssetSerializer(asset, context={'request': request})

        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AssetSerializer(asset, data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def assettypes(request):
    if request.method == 'GET':
        data = Assettype.objects.all()

        serializer = AssettypeSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['DELETE'])
def asset_control_matches(request):
    if request.method == 'DELETE':
        AssetControlMatch.objects.all().delete()
        property_metric = Metrics("Properties")
        property_metric.reset_metrics()
        control_metric = Metrics("Security_Controls")
        control_metric.reset_metrics()

        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def import_assets(request):
    if request.method == 'POST':
        try:
            file_import = FileImport()
            file_import.do_import()
            return Response(status=status.HTTP_200_OK)
        except:
            print(traceback.format_exc())
            return Response(status=status.HTTP_400_BAD_REQUEST)

