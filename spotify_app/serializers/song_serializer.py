from rest_framework import serializers
from spotify_app.models.songs_model import Song


class RandomSongSerializer(serializers.ModelSerializer):
    artist_id = serializers.CharField(source='artist.artist_id')
    artist_name = serializers.CharField(source='artist.name')
    song_title = serializers.CharField(source='title')
    duration = serializers.SerializerMethodField()
    album_cover = serializers.SerializerMethodField()  # ✅ now from Song.cover_url

    class Meta:
        model = Song
        fields = [
            'song_id',
            'song_title',
            'duration',
            'artist_id',
            'artist_name',
            'album_cover'
        ]

    def get_duration(self, obj):
        minutes = obj.duration // 60000
        seconds = (obj.duration % 60000) // 1000
        return f"{minutes}:{str(seconds).zfill(2)}"

    def get_album_cover(self, obj):
        return obj.cover_url  # ✅ direct from Song.cover_url


class SongDetailSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    album_cover = serializers.CharField(source='cover_url')
    album_name = serializers.CharField()

    class Meta:
        model = Song
        fields = [
            'song_id', 'title', 'duration', 'popularity', 'uri',
            'album_name', 'album_cover', 'artist'
        ]

    def get_artist(self, obj):
        return {
            'id': obj.artist.artist_id,
            'name': obj.artist.name,
            'picture_url': obj.artist.picture_url
        }

    def get_duration(self, obj):
        minutes = obj.duration // 60000
        seconds = (obj.duration % 60000) // 1000
        return f"{minutes}:{str(seconds).zfill(2)}"


    
class SongSimpleSerializer(serializers.ModelSerializer):
    album_cover = serializers.CharField(source='cover_url')
    song_name = serializers.CharField(source='title')
    album_name = serializers.CharField()  # ✅ fixed here

    class Meta:
        model = Song
        fields = ['song_id', 'song_name', 'duration', 'album_cover', 'album_name']