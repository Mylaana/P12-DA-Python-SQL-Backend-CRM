from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets 
from Client import serializers
from Client.models import Client
from UserProfile.models import UserProfile

class ClientViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on Client model"""
    serializer_class = serializers.ClientSerializer
    # permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    queryset = Client.objects.all()


    def perform_create(self, serializer):
        """handles create operation"""
        # getting the user from it's id
        user_id = self.request.data.get('ee_contact')
        user = UserProfile.objects.get(pk=user_id)
        serializer.save(ee_contact=user)
