from rest_framework import serializers
from UserProfile.models import UserProfile, Team

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'email','first_name', 'last_name', 'phone', 'team')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
                }
            }

    def create(self, validated_data):
        """Create and return new user"""
        user = UserProfile.objects.create_user(**validated_data)
        return user

class TeamSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""

    class Meta:
        model = Team
        fields = '__all__'
