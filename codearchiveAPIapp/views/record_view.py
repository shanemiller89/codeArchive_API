"""View module for handling requests about record"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Record

class RecordSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for records

    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Record
        url = serializers.HyperlinkedIdentityField(
            view_name='record',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'text', 'image', 'image_title', 'language', 'order', 'record_type_id', 'archive_id')


class Records(ViewSet):
    """Records for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Record instance
        """
        new_record = Record()
        new_record.title = request.data["title"]
        new_record.text = request.data["text"]
        new_record.image = request.data["image"]
        new_record.image_title = request.data["image_title"]
        new_record.language = request.data["language"]
        new_record.order = request.data["order"]
        new_record.record_type_id = request.data["record_type_id"]
        new_record.archive_id = request.data["archive_id"]

        new_record.save()

        serializer = RecordSerializer(new_record, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single record

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            record = Record.objects.get(pk=pk)
            record.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Log.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a record

        Returns:
            Response -- Empty body with 204 status code
        """
        record = Record.objects.get(pk=pk)
        record.title = request.data["title"]
        record.text = request.data["text"]
        record.image = request.data["image"]
        record.image_title = request.data["image_title"]
        record.language = request.data["language"]
        record.order = request.data["order"]

        record.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single record

        Returns:
            Response -- JSON serialized record instance
        """
        try:
            record = Record.objects.get(pk=pk)
            serializer = RecordSerializer(record, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to records resource

        Returns:
            Response -- JSON serialized list of records
        """
        records = Record.objects.all()
        
        archive = self.request.query_params.get('archive_id', None)

        order = self.request.query_params.get('order', None)

        if archive is not None:
            records = records.filter(archive_id=archive)
        if order is not None:
            records = records.filter(order=order)

        serializer = RecordSerializer(
            records,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)