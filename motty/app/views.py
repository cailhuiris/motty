from rest_framework.decorators import api_view

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from django.forms.models import model_to_dict
from django.db import connection
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from .utils import remove_last_slash
from .models import Action, Resource
from .serializers import ActionSerializer, ResourceSerializer

import json

# views
def main(request):
    return redirect(index)

def index(request):
    return render(request, 'app/index.html')

@api_view(['GET', 'POST'])
def create_action(request, resource_id):
    resource = Resource.objects.get(pk=resource_id)

    if request.method == 'GET':
        return render(request,'app/action/create.html', { 'resource': resource })
    else:
        body = request.data
        action = Action()
        serializer = ActionSerializer(action, data=body);

        if serializer.is_valid():
            serializer.save()
            messages.info(request, "The '{0}' action is successfully created.".format(body.get('name')))
            return redirect('index_view')
        else:
            return render(request, 'app/action/create.html', { 'resource': resource, 'errors': serializer.errors, 'form': body })

def action_view(request, id):
    action = Action.objects.get(pk=id)
    data = model_to_dict(action)
    data['resource'] = model_to_dict(Resource.objects.get(pk=data['resource']))
    data['editorType'] = get_editor_type(data['contentType'])

    return render(request, 'app/action/view.html', { 'id': id, 'action': data })

@api_view(['GET'])
def delete_action(request, id):
    try:
        action = Action.objects.get(pk=id)
        name = action.name
        action.delete()

        messages.info(request, "The '{0}' action is deleted.".format(name))
        return redirect('index_view')
    except ObjectDoesNotExist:
        messages.error(request, "No action to delete.")
        return redirect('index_view')

# api requests.
# resource api
@api_view(['GET'])
def resources(request):
    resource = Resource.objects.all()
    serializer = ResourceSerializer(resource, many=True)

    for idx, res in enumerate(serializer.data):
        for act_idx, act in enumerate(serializer.data[idx]['actions']):
            action = Action.objects.get(pk=act)
            action_serializer = ActionSerializer(action)
            serializer.data[idx]['actions'][act_idx] = action_serializer.data

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def delete_resource(request, id):
    try:
        resource = Resource.objects.get(pk=id)
        resource.delete()

        return HttpResponse('The resource number {0} is successfully deleted'.format(id))
    except ObjectDoesNotExist:
        return HttpResponse('No resoruce to delete.', status=404)

@api_view(['POST'])
def save_resource(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        resource = Resource() if data.get('id') is None else Resource.objects.get(pk=data['id'])
        serializer = ResourceSerializer(resource, data=data) if data.get('id') is None else \
            ResourceSerializer(resource, data=data, partial=True)

        if serializer.is_valid() :
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, status=400)
    except ObjectDoesNotExist:
        return HttpResponse("No resource to save.", status=404 )

# fake responses.
@csrf_exempt
def return_fake_request(request, endpoint):
    return HttpResponse('Under construction.')

def get_editor_type(content_type):
    json_editors = ['application/json', 'application/javascript']
    xml_editors = ['text/xml', 'application/xml']
    html_editors = ['text/html']

    if content_type in json_editors:
        return 'json';

    if content_type in xml_editors:
        return 'xml';

    if content_type in html_editors:
        return 'xml';
    
    return 'text';