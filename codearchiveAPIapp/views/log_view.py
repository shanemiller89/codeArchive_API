"""View module for handling requests about logs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Log, Archive, LogArchive, Coder
from .archive_view import ArchiveSerializer
from .log_archive_view import LogArchiveSerializer

class LogSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for logs

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    archives = ArchiveSerializer(many=True, read_only=True)

    class Meta:
        model = Log
        url = serializers.HyperlinkedIdentityField(
            view_name='library',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'reference', 'log_type_id', 'coder_id', 'archives')

        depth = 2

class Logs(ViewSet):
    """Logs for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Log instance
        """

        archive_item = LogArchive()
        new_log = Log()
        new_log.title = request.data["title"]
        new_log.reference = request.data["reference"]
        new_log.log_type_id = request.data["log_type_id"]
        new_log.coder =  Coder.objects.get(user=request.auth.user)
        new_log.save()
        new_archive = Archive()
        new_archive.title = request.data["title"]
        new_archive.link = request.data["link"]
        new_archive.save()
        archive_item.log = new_log
        archive_item.archive = new_archive

        archive_item.save()

        serializer = LogArchiveSerializer(archive_item, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single log

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            log = Log.objects.get(pk=pk)
            log.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Log.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for an log

        Returns:
            Response -- Empty body with 204 status code
        """
        log = Log.objects.get(pk=pk)
        log.title = request.data["title"]
        log.reference = request.data["reference"]

        log.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single log

        Returns:
            Response -- JSON serialized log instance
        """
        try:
            log = Log.objects.get(pk=pk)
            serializer = LogSerializer(log, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to log resource

        Returns:
            Response -- JSON serialized list of logs
        """
        logs = Log.objects.all()
        coder = Coder.objects.get(user=request.auth.user)
        logs = Log.objects.filter(coder=coder)

        log_type = self.request.query_params.get('log_type_id', None)

        if log_type is not None:
            logs = logs.filter(log_type_id=log_type)

        serializer = LogSerializer(
            logs,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)