from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from Event.serializers import EventSerializer
from Event.models import Event


class EventViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on UserProfile model"""
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    queryset = Event.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Event.objects.all()
        name = self.request.query_params.get('name')

        if name is not None:
            queryset = Event.objects.filter(name=name.replace("/",""))
        return queryset
