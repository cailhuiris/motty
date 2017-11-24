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
def save_action(request, resource_id, action_id=None):
    resource = Resource.objects.get(pk=resource_id)

    if request.method == 'GET':
        if action_id is None:
            return render(request,'app/action/form.html', { 
                        'resource': resource 
                   })
        else:
            action = Action.objects.get(pk=action_id)
            return render(request,'app/action/form.html', { 
                        'resource': resource,
                        'action': action
                   })
    else:
        body = request.data
        action = Action() if body.get('id') is None else Action.objects.get(pk=body.get('id'))
        serializer = ActionSerializer(action, data=body);

        if serializer.is_valid():
            serializer.save()
            messages.info(request, "The '{0}' action is successfully saved.".format(body.get('name')))
            return redirect('index_view')
        else:
            action_id = body.get('id')
            if action_id is None:
                return render(request, 'app/action/form.html', { 'resource': resource, 'errors': serializer.errors, 'form': body })
            else:
                return render(request, 'app/action/form.html', { 'resource': resource, 'action': action, 'errors': serializer.errors, 'form': body })

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
            serializer.data[idx]['actions'][act_idx]['readableType'] = to_readable_type(action_serializer.data['contentType'])

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def delete_resource(request, id):
    try:
        resource = Resource.objects.get(pk=id)
        resource.delete()

        messages.info(request, "The '{0}' resource is successfully deleted.".format(resource.name))
        return redirect('index_view')
    except ObjectDoesNotExist:
        messages.info(request, "No resource to delete.")
        return redirect('index_view')

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
    import re;

    method = request.method
    endpoint = '/' + endpoint
    result = re.match("^(?P<resource>\/[a-z0-9A-Z-_]+)(?P<action>\/[a-z0-9A-Z-_/]+)?", endpoint)

    resource_url = result.group('resource')
    action_url = result.group('action')

    if action_url is None:
        root_action = resource_url[1:]
        root_resource = Resource.objects.filter(url='/')[0]
        query = Action.objects.filter(resource=root_resource.id, url=root_action, method=method)
        if len(query) > 0:
            action = query[0]
            return HttpResponse(action.body, content_type=action.contentType)
    else:
        r_query = Resource.objects.filter(url=resource_url)
        if len(r_query) > 0:
            resource = r_query[0]
            query = Action.objects.filter(resource=resource.id, url=action_url, method=method)
            if len(query) > 0:
                action = query[0]
                return HttpResponse(action.body, content_type=action.contentType)

    return HttpResponse("Oops. There is no such action.", status=404)

# utils
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

def to_readable_type(content_type):
    return get_editor_type(content_type).upper();