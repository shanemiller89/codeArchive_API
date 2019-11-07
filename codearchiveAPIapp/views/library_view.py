"""View module for handling requests about libraries"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Library, Coder
from .archive_view import ArchiveSerializer

class SubLibrarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Library
        url = serializers.HyperlinkedIdentityField(
            view_name='sub_library',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'link', 'image', 'image_title', 'library_type_id', 'coder_id')

        depth = 1

class LibrarySerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for libraries

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    sub_libraries = SubLibrarySerializer(many=True, read_only=True)
    archives =  ArchiveSerializer(many=True, read_only=True)

    class Meta:
        model = Library
        url = serializers.HyperlinkedIdentityField(
            view_name='library',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'link', 'image', 'image_title', 'parent_library_id', 'library_type_id', 'coder_id', 'sub_libraries', 'archives')

        depth = 1

class Libraries(ViewSet):
    """Libraries for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Library instance
        """
        new_library = Library()
        new_library.title = request.data["title"]
        new_library.link = request.data["link"]
        new_library.image = request.data["image"]
        new_library.image_title = request.data["image_title"]
        new_library.parent_library_id = request.data["parent_library_id"]
        new_library.library_type_id = request.data["library_type_id"]
        new_library.coder = Coder.objects.get(user=request.auth.user)
        # new_library.coder = coder

        new_library.save()

        serializer = LibrarySerializer(new_library, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single library

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            library = Library.objects.get(pk=pk)
            library.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Library.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a library

        Returns:
            Response -- Empty body with 204 status code
        """
        library = Library.objects.get(pk=pk)
        library.title = request.data["title"]
        library.link = request.data["link"]
        library.image = request.data["image"]
        library.image_title = request.data["image_title"]

        library.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single library

        Returns:
            Response -- JSON serialized library instance
        """
        try:
            library = Library.objects.get(pk=pk)
            serializer = LibrarySerializer(library, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to library resource

        Returns:
            Response -- JSON serialized list of libraries
        """
        libraries = Library.objects.all()
        coder = Coder.objects.get(user=request.auth.user)
        libraries = Library.objects.filter(coder=coder)

        parent_library = self.request.query_params.get('parent_library_id', None)
        library_type = self.request.query_params.get('library_type_id', None)



        if parent_library is not None:
            libraries = libraries.filter(parent_library_id=parent_library)
        if library_type is not None:
            libraries = libraries.filter(library_type_id=library_type)

        serializer = LibrarySerializer(
            libraries,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)