from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Metric
from .serializers import MetricSerializer
from .graph_controller import GraphController

@api_view(['GET', 'DELETE'])
def metrics(request):
    if request.method == 'GET':
        data = Metric.objects.all()

        serializer = MetricSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    elif request.method == 'DELETE':
        Metric.objects.all().delete()
        
        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def create_graphs(request):
    if request.method == 'POST':
        graph_controller = GraphController()
        graph_controller.create_graphs()

        return Response(status=status.HTTP_200_OK)
