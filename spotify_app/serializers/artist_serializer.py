from rest_framework import serializers
from spotify_app.models.songs_model import Artist, Song
import random

class SongSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['song_id', 'title', 'uri', 'duration', 'explicit', 'popularity', 'cover_url']

class ArtistCustomSerializer(serializers.ModelSerializer):
    songs = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ['artist_id', 'name', 'picture_url', 'followers', 'popularity', 'songs']

    def get_songs(self, artist):
        songs = list(Song.objects.filter(artist=artist))
        random.shuffle(songs)
        selected = songs[:20]
        return SongSimpleSerializer(selected, many=True).data
