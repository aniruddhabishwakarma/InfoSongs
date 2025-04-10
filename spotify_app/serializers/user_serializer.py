# spotify_app/serializers.py
from rest_framework import serializers
from spotify_app.models.auth_model import CustomUser  # adjust import path if needed
from ..models.songs_model import Song
from ..models.songs_model import Like  # ✅ bring in the Like model

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
    
class LikedSongSerializer(serializers.ModelSerializer):
    album_cover = serializers.CharField(source='cover_url')
    song_name = serializers.CharField(source='title')
    album_name = serializers.CharField()
    uri = serializers.CharField()

    class Meta:
        model = Song
        fields = ['song_id', 'song_name', 'duration', 'album_cover', 'album_name', 'uri']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
