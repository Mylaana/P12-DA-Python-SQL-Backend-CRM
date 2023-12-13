from rest_framework import serializers
from Contract.models import Contract
from UserProfile.models import UserProfile
from Client.models import Client

class ContractSerializer(serializers.ModelSerializer):
    """Serializes Contract model"""
    epicevents_contact_name = serializers.SerializerMethodField()
    client_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Contract
        fields = (
            'id',
            'client',
            'client_name',
            'information',
            'ee_contact',
            'epicevents_contact_name',
            'value_total_price',
            'value_rest_to_pay',
            'date_creation',
            'status_is_active'
            )

    def get_epicevents_contact_name(self, obj):
        if obj.ee_contact is None:
            return
        return obj.ee_contact.username
    
    def get_client_name(self, obj):
        return obj.client.name