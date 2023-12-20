from rest_framework import serializers
from Client import models


class ClientSerializer(serializers.ModelSerializer):
    """Serializes Client model"""
    ee_contact_name = serializers.SerializerMethodField()
    class Meta:
        model = models.Client
        fields = '__all__'

    def get_ee_contact_name(self, obj):
        if obj.ee_contact is None:
            return
        return obj.ee_contact.username
