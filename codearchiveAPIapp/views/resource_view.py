"""View module for handling requests about resource"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Resource

class ResourceSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for resources

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Resource
        url = serializers.HyperlinkedIdentityField(
            view_name='resource',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'link', 'description', 'resource_type_id', 'archive_id')


class Resources(ViewSet):
    """Resource for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Resource instance
        """
        new_resource = Resource()
        new_resource.title = request.data["title"]
        new_resource.link = request.data["link"]
        new_resource.description = request.data["description"]
        new_resource.resource_type_id = request.data["resource_type_id"]
        new_resource.archive_id = request.data["archive_id"]

        new_resource.save()

        serializer = ResourceSerializer(new_resource, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single resource

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            resource = Resource.objects.get(pk=pk)
            resource.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Resource.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a resource

        Returns:
            Response -- Empty body with 204 status code
        """
        resource = Resource.objects.get(pk=pk)
        resource.title = request.data["title"]
        resource.link = request.data["link"]
        resource.description = request.data["description"]

        resource.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single resource

        Returns:
            Response -- JSON serialized resource instance
        """
        try:
            resource = Resource.objects.get(pk=pk)
            serializer = ResourceSerializer(resource, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to resource resource

        Returns:
            Response -- JSON serialized list of resources
        """
        resources = Resource.objects.all()

        serializer = ResourceSerializer(
            resources,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)