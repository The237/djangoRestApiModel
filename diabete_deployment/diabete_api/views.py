
import pathlib
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
import joblib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import numpy as np
import json
from diabete_api.NpEncoder import NpEncoder

# Load the model from static folder

abspath = pathlib.Path('../model/diabete_detector_model.pkl').absolute()

loaded_model = joblib.load(open(abspath, 'rb'))


@api_view(['GET'])
def index(request):
    return_data = {
        "error_code": "0",
        "info": "success",
    }
    return Response(return_data)


@api_view(['GET'])
def prediction(request):
    return render(request, 'predictions/index.html')

@api_view(['POST'])
def predict_patient_status(request):
    try:
        response_data = {}
        # load the request data
        patient_json_info = request.data

        # Retrieve all the values from the json data
        patient_info = np.array(list(patient_json_info.values()))

        # Make prediction
        patient_status = loaded_model.predict([patient_info])

        # Model confidence score
        model_confidence_score=  np.max(loaded_model.predict_proba([patient_info]))
        
        model_prediction = {
            'info': 'success',
            'patient_status': patient_status[0],
            'model_confidence_proba': float("{:.2f}".format(model_confidence_score*100))
        }

    except ValueError as ve:
        model_prediction = {
            'error_code' : '-1',
            "info": str(ve)
        }
    
    response_data['info'] = model_prediction['info']
    response_data['patient_status'] = model_prediction['patient_status']
    response_data['model_confidence_proba'] = model_prediction['model_confidence_proba']
    
    return HttpResponse(
        json.dumps(response_data,
        cls=NpEncoder), 
        content_type = 'application/json'
    )
    

    