"""View module for handling requests about log archives"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import LogArchive


class LogArchiveSerializer(serializers.HyperlinkedModelSerializer):

    """JSON serializer for log archives

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = LogArchive
        url = serializers.HyperlinkedIdentityField(
            view_name='log_archive',
            lookup_field='id'
        )
        fields = ('id', 'url', 'log_id', 'archive_id', 'log', 'archive')

        depth = 2


class LogArchives(ViewSet):
    """LogArchives for codeArchive"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single archives

        Returns:
            Response -- JSON serialized log archive instance
        """
        try:
            log_archive = LogArchive.objects.get(pk=pk)
            serializer = LogArchiveSerializer(log_archive, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to log archives resource

        Returns:
            Response -- JSON serialized list of log archives
        """
        log_archives = LogArchive.objects.all()
        serializer = LogArchiveSerializer(
            log_archives,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)