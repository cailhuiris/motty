from .models import Action, Resource
from .utils import remove_last_slash
from rest_framework import serializers

import datetime

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'resource', 'name', 'url', 'method', 'contentType', 'body', 'created_at')

    # def create(self, validated_data):
    #     validated_data['url'] = remove_last_slash(validated_data['url'])
    #     return Action.objects.create(**validated_data)

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('id', 'name', 'url', 'actions')
        read_only_fields = ('actions', )

    def get_validation_exclusions(self):
        exclusions = super(FavoriteListSerializer, self).get_validation_exclusions()
        return exclusions + ['actions']

def json_serializer(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    return str(obj)