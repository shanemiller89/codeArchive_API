"""View module for handling requests about log types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import LogType


class LogTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for log types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = LogType
        url = serializers.HyperlinkedIdentityField(
            view_name='logtype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'type')


class LogTypes(ViewSet):
    """LogTypes for codeArchive"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for log type

        Returns:
            Response -- JSON serialized log type instance
        """
        try:
            log_type = LogType.objects.get(pk=pk)
            serializer = LogTypeSerializer(log_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to log type resource

        Returns:
            Response -- JSON serialized list of log types
        """
        log_types = LogType.objects.all()
        serializer = LogTypeSerializer(
            log_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)