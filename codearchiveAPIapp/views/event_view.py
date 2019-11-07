"""View module for handling requests about events"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from codearchiveAPIapp.models import Event, Coder


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for events

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Event
        url = serializers.HyperlinkedIdentityField(
            view_name='event',
            lookup_field='id'
        )
        fields = ('id', 'url', 'title', 'date', 'location', 'description', 'link', 'reference', 'coder_id')

        depth = 1

class Events(ViewSet):
    """Events for codeArchive"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Event instance
        """
        new_event = Event()
        new_event.title = request.data["title"]
        new_event.date = request.data["date"]
        new_event.location = request.data["location"]
        new_event.description = request.data["description"]
        new_event.link = request.data["link"]
        new_event.reference = request.data["reference"]
        new_event.coder = Coder.objects.get(user=request.auth.user)


        new_event.save()

        serializer = EventSerializer(new_event, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single event

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Log.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for an event

        Returns:
            Response -- Empty body with 204 status code
        """
        event = Event.objects.get(pk=pk)
        event.title = request.data["title"]
        event.date = request.data["date"]
        event.location = request.data["location"]
        event.description = request.data["description"]
        event.link = request.data["link"]
        event.reference = request.data["reference"]

        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single event

        Returns:
            Response -- JSON serialized event instance
        """
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to event resource

        Returns:
            Response -- JSON serialized list of events
        """
        events = Event.objects.all()
        coder = Coder.objects.get(user=request.auth.user)
        events = Event.objects.filter(coder=coder)

        serializer = EventSerializer(
            events,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)