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
