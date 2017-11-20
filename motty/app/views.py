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
    return render(request, 'app/action/view.html')

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

# action api
# @csrf_exempt
# @api_view(['POST'])
# def save_action(request):
#     try:
#         data = json.loads(request.body.decode('utf-8'))
#         action = Action() if data.get('id') is None else Action.objects.get(pk=data['id'])
#         serializer = ActionSerializer(action, data=data) if data.get('id') is None else \
#             ActionSerializer(action, data=data, partial=True)

#         if serializer.is_valid() :
#             action = serializer.save()
#             return JsonResponse(serializer.data, safe=False)
#         else:
#             return JsonResponse(serializer.errors, status=400)
#     except ObjectDoesNotExist:
#         return HttpResponse("No action to save.", status=404)

@api_view(['GET'])
def delete_action(request, id):
    try:
        action = Action.objects.get(pk=id)
        action.delete()
        return HttpResponse('deleted.')
    except ObjectDoesNotExist:
        return HttpResponse('There is no data to delete.')

@csrf_exempt
@api_view(['POST'])
def delete_all(request):
    res = json.loads(request.body.decode('utf-8'))
    ids = res['ids']
    with connection.cursor() as cursor:
        cursor.execute('DELETE FROM app_action WHERE id in ' + "(" + ",".join(map(str, ids)) + ")")

    return HttpResponse("your requests are successfully conducted.")


@api_view(['GET'])
def get_action(request, id):
    action = Action.objects.get(pk=id)
    return JsonResponse(model_to_dict(action))

# fake responses.
@csrf_exempt
def return_fake_request(request, endpoint):
    endpoint = "/" + endpoint
    actions = Action.objects.filter(url=remove_last_slash(endpoint), method=request.method)
    if len(actions) > 0:
        action = actions[0]
        return HttpResponse(action.body, content_type=action.contentType)
    else:
        return HttpResponse('No such response exists.', status=404)