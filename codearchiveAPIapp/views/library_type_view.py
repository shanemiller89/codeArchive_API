"""View module for handling requests about library types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import LibraryType


class LibraryTypeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for library types

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = LibraryType
        url = serializers.HyperlinkedIdentityField(
            view_name='librarytype',
            lookup_field='id'
        )
        fields = ('id', 'url', 'type')


class LibraryTypes(ViewSet):
    """Library Types for codeArchive"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for library type

        Returns:
            Response -- JSON serialized library type instance
        """
        try:
            library_type = LibraryType.objects.get(pk=pk)
            serializer = LibraryTypeSerializer(library_type, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to library types resource

        Returns:
            Response -- JSON serialized list of library types
        """
        library_types = LibraryType.objects.all()
        serializer = LibraryTypeSerializer(
            library_types,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)