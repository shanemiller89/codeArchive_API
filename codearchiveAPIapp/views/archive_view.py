"""View module for handling requests about archives"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Archive
from codearchiveAPIapp.models import Library
from codearchiveAPIapp.models import LibraryArchive
from .library_archive_view import LibraryArchiveSerializer
from .record_view import RecordSerializer
from .resource_view import ResourceSerializer


class ArchiveSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for archives

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    records =  RecordSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Archive
        url = serializers.HyperlinkedIdentityField(
            view_name='archive',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'link', 'records', 'resources')

        depth = 1

class Archives(ViewSet):
    """Archives for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Archive instance
        """

        archive_item = LibraryArchive()
        archive_item.library = Library.objects.get(pk=request.data["library_id"])
        new_archive = Archive()
        new_archive.title = request.data["title"]
        new_archive.link = request.data["link"]
        new_archive.save()
        archive_item.archive = new_archive

        archive_item.save()

        serializer = LibraryArchiveSerializer(archive_item, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single archive

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            archive = Archive.objects.get(pk=pk)
            archive.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Library.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, pk=None):
        """Handle PUT requests for an archive

        Returns:
            Response -- Empty body with 204 status code
        """
        archive = Archive.objects.get(pk=pk)
        archive.title = request.data["title"]
        archive.link = request.data["link"]

        archive.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single archives

        Returns:
            Response -- JSON serialized archive instance
        """
        try:
            archive = Archive.objects.get(pk=pk)
            serializer = ArchiveSerializer(archive, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to archives resource

        Returns:
            Response -- JSON serialized list of archives
        """
        archives = Archive.objects.all()
        serializer = ArchiveSerializer(
            archives,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)