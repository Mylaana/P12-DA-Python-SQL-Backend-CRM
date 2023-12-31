from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from Client import serializers
from Client.models import Client
from UserProfile.models import UserProfile
from EpicEvents import permissions


class ClientViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on Client model"""
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAuthenticated, permissions.ClientPermisison]
    queryset = Client.objects.all()

    def perform_create(self, serializer):
        """handles create operation"""
        # getting the user from it's id
        user_id = self.request.data.get('ee_contact')
        user = UserProfile.objects.get(pk=user_id)
        serializer.save(ee_contact=user)

    def get_queryset(self):
        """
        Optionally restricts the returned clients,
        by filtering against a `name` query parameter in the URL.
        """
        queryset = Client.objects.all()
        name = self.request.query_params.get('name')

        if name is not None:
            queryset = Client.objects.filter(name=name.replace("/",""))
        return queryset