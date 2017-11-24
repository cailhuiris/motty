from django.db.models import Q
from rest_framework import serializers

import datetime

from .models import Action, Resource
from .utils import remove_last_slash

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'resource', 'name', 'url', 'method', 'contentType', 'body', 'created_at')

    def validate(self, data):
        action_id = data.get('id')
        resource = data['resource']
        url = data['url']
        
        if resource.url == '/':
            if '/' in url:
                raise serializers.ValidationError("Action url must have just one slash at the beginning of it.")
            
            combined = resource.url + url
            resources = Resource.objects.filter(url=combined)
            if len(resources) > 0 :
                resource = resources[0]
                raise serializers.ValidationError("This url is same with the `%s` resource's url, URL must be unique cross the app." % (resource.name))
        else:
            if resource.url != '/' and url[0] != '/':
                raise serializers.ValidationError("Action url must start with '/', ex) '/all', '/1/product'")

        if action_id is not None:
            actions = Action.objects.filter(~Q(id=action_id), resource=resource.id, url=url)
            if len(actions) > 0:
                raise serializers.ValidationError("Action with this url already exists.")

        return data

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'url', 'actions')
        read_only_fields = ('actions', )

    def validate_url(self, value):
        if value[0] != '/':
            raise serializers.ValidationError("URL must start with '/', ex) '/users'")

        when_slash_more_than_one = len(value.split('/')) > 2
        if when_slash_more_than_one:
            raise serializers.ValidationError("Resource url must have just one slash at the beginning of it.")

        return value;

    def get_validation_exclusions(self):
        exclusions = super(FavoriteListSerializer, self).get_validation_exclusions()
        return exclusions + ['actions']

def json_serializer(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    return str(obj)