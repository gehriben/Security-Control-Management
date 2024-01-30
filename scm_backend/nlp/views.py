import traceback
import json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from nlp.file_reader import FileReader
from nlp.nlp.nlp_controller_security_controls import NLPControllerSecurityControls
from nlp.nlp.nlp_controller_properties import NLPControllerProperties
from nlp.matching.matching_controller import MatchingController
from nlp.matching.tfidf_matching import TFIDFMatching
from nlp.matching.matching_results_handler import MatchingResultsHandler

# Create your views here.

@api_view(['POST'])
def import_controls(request):
    if request.method == 'POST':
        file_reader = FileReader()
        result = file_reader.read_nist_controls()
        if result == "SUCCESS":
            return Response(status=status.HTTP_200_OK)

        return Response("Import of controls failed!", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def analyse_controls(request):
    if request.method == 'POST':
        nlp = NLPControllerProperties()
        nlp.analyse_properties()

        nlp_controls = NLPControllerSecurityControls()
        nlp_controls.analyse_security_controls()

        return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def match_controls(request):
    if request.method == 'POST':
        """control_matching = ControlMatching()
        matching_controls = control_matching.match()"""

        matching_controller = MatchingController()
        matching_controls = matching_controller.match()

        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def tfidf_matching(request):
        if request.method == 'POST':
            tfidf_matching = TFIDFMatching()
            tfidf_matching.start_matching()

            return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def matching_controls_with_assets(request):
    if request.method == 'GET':
        matching_results_handler = MatchingResultsHandler()
        matching_controls = matching_results_handler.get_matching_results_with_assets_per_control()

        return Response(matching_controls)

@api_view(['GET'])
def matching_controls_with_asset(request, asset_id):
    if request.method == 'GET':
        matching_results_handler = MatchingResultsHandler()
        matching_controls = matching_results_handler.get_matching_results_with_per_asset(asset_id)

        return Response(matching_controls)
