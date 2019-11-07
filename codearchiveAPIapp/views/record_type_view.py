"""View module for handling requests about record type"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import RecordType


class RecordTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for record types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = RecordType
        url = serializers.HyperlinkedIdentityField(
            view_name='recordtype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'type')


class RecordTypes(ViewSet):
    """Record Types for codeArchive"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for record

        Returns:
            Response -- JSON serialized record type instance
        """
        try:
            record_type = RecordType.objects.get(pk=pk)
            serializer = RecordTypeSerializer(record_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to record type resource

        Returns:
            Response -- JSON serialized list of record types
        """
        record_types = RecordType.objects.all()
        serializer = RecordTypeSerializer(
            record_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)