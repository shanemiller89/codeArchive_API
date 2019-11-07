"""View module for handling requests about library archives"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import LibraryArchive
# from codearchiveAPIapp.views import LibrarySerializer
# from codearchiveAPIapp.views import ArchiveSerializer


class LibraryArchiveSerializer(serializers.HyperlinkedModelSerializer):

    # library = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    # archive = ArchiveSerializer(many=True)

    """JSON serializer for library archives

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = LibraryArchive
        url = serializers.HyperlinkedIdentityField(
            view_name='libraryarchive',
            lookup_field='id'
        )
        fields = ('id', 'url', 'library_id', 'archive_id', 'library', 'archive')

        depth = 1


class LibraryArchives(ViewSet):
    """LibraryArchives for codeArchive"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single library archive

        Returns:
            Response -- JSON serialized LibraryArchive instance
        """
        try:
            library_archive = LibraryArchive.objects.get(pk=pk)
            serializer = LibraryArchiveSerializer(library_archive, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to library archive resource

        Returns:
            Response -- JSON serialized list of library archives
        """
        library_archives = LibraryArchive.objects.all()
        serializer = LibraryArchiveSerializer(
            library_archives,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)