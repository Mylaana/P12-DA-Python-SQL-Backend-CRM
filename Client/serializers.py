from rest_framework import serializers
from Client import models


class ClientSerializer(serializers.ModelSerializer):
    """Serializes Client model"""

    class Meta:
        model = models.Client
        fields = '__all__'
