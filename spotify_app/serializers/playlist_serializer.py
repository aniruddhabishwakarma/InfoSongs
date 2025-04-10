from rest_framework import serializers
from ..models.user_model import Playlist, PlaylistSong
from ..models.songs_model import Song

class PlaylistSerializer(serializers.ModelSerializer):
    cover_url = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'description', 'created_at', 'cover_url']

    def get_cover_url(self, playlist):
        first_song = playlist.songs.select_related('song').first()
        return first_song.song.cover_url if first_song and first_song.song.cover_url else None




class PlaylistDetailSerializer(serializers.ModelSerializer):
    song_id = serializers.CharField(write_only=True)
    song_title = serializers.CharField(source='song.title', read_only=True)
    album_cover = serializers.CharField(source='song.cover_url', read_only=True)

    class Meta:
        model = PlaylistSong
        fields = ['id', 'song_id', 'song_title', 'album_cover', 'added_at']

    def validate_song_id(self, value):
        try:
            song = Song.objects.get(song_id=value)
            return song
        except Song.DoesNotExist:
            raise serializers.ValidationError("Song with this ID does not exist.")

    def create(self, validated_data):
        song = validated_data.pop('song_id')
        playlist = validated_data['playlist']
        return PlaylistSong.objects.create(playlist=playlist, song=song)
