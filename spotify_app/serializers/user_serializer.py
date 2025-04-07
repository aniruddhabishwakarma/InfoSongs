# spotify_app/serializers.py
from rest_framework import serializers
from spotify_app.models.auth_model import CustomUser  # adjust import path if needed

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'full_name',
            'profile_picture',
            'locale',
            'is_google_user',
        ]

    def get_full_name(self, obj):
        # Combine safely even if one of them is missing
        return f"{obj.given_name or ''} {obj.family_name or ''}".strip()
