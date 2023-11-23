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


    def get_queryset(self):
        """
        Optionally restricts the returned queryset,
        by filtering against a `information` query parameter in the URL.
        """
        queryset = Contract.objects.all()
        information = self.request.query_params.get('information')

        if information is not None:
            queryset = Contract.objects.filter(information=information.replace("/",""))
        return queryset
