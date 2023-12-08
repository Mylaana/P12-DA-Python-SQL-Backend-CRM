from rest_framework import serializers
from Event.models import Event

class EventSerializer(serializers.ModelSerializer):
    """Serializes Event model"""
    ee_contact_name = serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = "__all__"

    def get_ee_contact_name(self, obj):
        if obj.ee_contact is None:
            return
        return obj.ee_contact.username