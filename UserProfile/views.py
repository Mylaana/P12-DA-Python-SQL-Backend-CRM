from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from UserProfile.serializers import UserProfileSerializer, TeamSerializer
from UserProfile.models import UserProfile, Team


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on UserProfile model"""
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    permission_classes = [IsAuthenticated,]
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = UserProfile.objects.all()
        username = self.request.query_params.get('username')

        if username is not None:
            queryset = UserProfile.objects.filter(username=username.replace("/",""))
        return queryset

class TeamViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on Team model"""
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated,]
    queryset = Team.objects.all()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Team.objects.all()
        name = self.request.query_params.get('name')

        if name is not None:
            queryset = Team.objects.filter(name=name.replace("/",""))
        return queryset