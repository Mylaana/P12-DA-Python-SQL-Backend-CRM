from rest_framework import serializers
from UserProfile.models import UserProfile, Team

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""
    team_name = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'password', 'email','first_name', 'last_name', 'phone', 'team', 'team_name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
                }
            }

    def get_team_name(self, obj):
        return obj.team.name

    def create(self, validated_data):
        """Create and return new user"""
        user = UserProfile.objects.create_user(**validated_data)
        return user
    
    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)

class TeamSerializer(serializers.ModelSerializer):
    """Serializes UserProfile model"""

    class Meta:
        model = Team
        fields = '__all__'
