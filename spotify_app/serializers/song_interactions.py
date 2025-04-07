from rest_framework import serializers
from ..models.songs_model import Like, Comment

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'song', 'timestamp']
        read_only_fields = ['id', 'timestamp', 'user']

class CommentSerializer(serializers.ModelSerializer):
    display_name = serializers.SerializerMethodField()
    profile_picture = serializers.URLField(source='user.profile_picture', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'content', 'timestamp', 'display_name', 'profile_picture']

    def get_display_name(self, obj):
        # Safely fall back to first_name or username if given_name is None
        return obj.user.given_name or obj.user.first_name or obj.user.username