from rest_framework import serializers
from Event.models import Event

class EventSerializer(serializers.ModelSerializer):
    """Serializes Event model"""

    class Meta:
        model = Event
        fields = "__all__"
