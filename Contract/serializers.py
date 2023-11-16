from rest_framework import serializers
from Contract.models import Contract

class ContractSerializer(serializers.ModelSerializer):
    """Serializes Contract model"""
    class Meta:
        model = Contract
        fields = '__all__'

