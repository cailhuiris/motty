from .models import Action, Resource
from .utils import remove_last_slash
from rest_framework import serializers

import datetime

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'resource', 'name', 'url', 'method', 'contentType', 'body', 'created_at')

    def validate_url(self, value):
        if value[0] != '/':
            raise serializers.ValidationError("URL must star with '/', ex) '/all'")
        
        return value

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'url', 'actions')
        read_only_fields = ('actions', )

    def validate_url(self, value):
        if value[0] != '/':
            raise serializers.ValidationError("URL must start with '/', ex) '/users'")

        return value;

    def get_validation_exclusions(self):
        exclusions = super(FavoriteListSerializer, self).get_validation_exclusions()
        return exclusions + ['actions']

def json_serializer(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    return str(obj)