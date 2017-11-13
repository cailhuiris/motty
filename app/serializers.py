from .models import Action
from rest_framework import serializers
import datetime

class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ('id', 'name', 'url', 'method', 'contentType', 'body', 'created_at')

def json_serializer(obj):
    """Default JSON serializer."""

    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S.%f')
    return str(obj)