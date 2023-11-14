from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from UserProfile.serializers import UserProfileSerializer, TeamSerializer
from UserProfile.models import UserProfile, Team


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on UserProfile model"""
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    queryset = UserProfile.objects.all()
    """
    def perform_create(self, serializer):
        handles create operation
        # getting the user from it's id
        user_id = self.request.data.get('ee_contact')
        user = UserProfile.objects.get(pk=user_id)
        serializer.save(ee_contact=user)
    """
class TeamViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on Team model"""
    serializer_class = TeamSerializer
    # permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    queryset = Team.objects.all()
