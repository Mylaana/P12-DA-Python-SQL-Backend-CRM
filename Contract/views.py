from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action

from Contract.serializers import ContractSerializer
from Contract.models import Contract


class ContractViewSet(viewsets.ModelViewSet):
    """Handle CRUD operations on UserProfile model"""
    serializer_class = ContractSerializer
    # permission_classes = [IsAuthenticated, permissions.UpdateRessource]
    queryset = Contract.objects.all()
