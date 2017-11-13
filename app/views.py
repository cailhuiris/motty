from rest_framework.decorators import api_view

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.forms.models import model_to_dict
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from .models import Action
from .serializers import ActionSerializer

import json

# main view
def main(request):
    return redirect(index)

def index(request):
    return render(request, 'app/index.html')

# api requests.
@api_view(['GET'])
def actions(request):
    actions = Action.objects.values()
    serializer = ActionSerializer(actions, many=True)
    return JsonResponse(serializer.data, safe=False);

@csrf_exempt
@api_view(['POST'])
def create_new_action(request):
    data = json.loads(request.body.decode('utf-8'))
    serializer = ActionSerializer(data=data)
    if serializer.is_valid() :
        serializer.save()
        return HttpResponse('data is successfully saved')
    else:
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@api_view(['POST'])
def edit_action(request, id):
    data = json.loads(request.body.decode('utf-8'))
    serializer = ActionSerializer(data=data)
    if serializer.is_valid() :
        _action = serializer.data
        try:
            action = Action.objects.get(pk=id)
            action.name = _action['name']
            action.url = _action['url']
            action.method = _action['method']
            action.contentType = _action['contentType']
            action.body = _action['body']
            action.save()
            return HttpResponse('data is successfully saved.')
        except ObjectDoesNotExist:
            return HttpResponse('There is no data to udpate.', status=404)
    else:
        return JsonResponse(serializer.errors, status=400)

@api_view(['GET'])
def delete_action(request, id):
    try:
        action = Action.objects.get(pk=id)
        action.delete()
        return HttpResponse('deleted.')
    except ObjectDoesNotExist:
        return HttpResponse('There is no data to delete.')

@api_view(['GET'])
def get_action(request, id):
    action = Action.objects.get(pk=id)
    return JsonResponse(model_to_dict(action))

# fake responses.
def return_fake_request(request, endpoint):
    pass