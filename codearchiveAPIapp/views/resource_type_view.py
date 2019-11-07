"""View module for handling requests about resource types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import ResourceType

class ResourceTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for resource types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = ResourceType
        url = serializers.HyperlinkedIdentityField(
            view_name='resourcetype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'type')


class ResourceTypes(ViewSet):
    """Resources for codeArchive"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single resource type

        Returns:
            Response -- JSON serialized resource type instance
        """
        try:
            resource_type = ResourceType.objects.get(pk=pk)
            serializer = ResourceTypeSerializer(resource_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to resource type resource

        Returns:
            Response -- JSON serialized list of resource type
        """
        resource_types = ResourceType.objects.all()
        serializer = ResourceTypeSerializer(
            resource_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)