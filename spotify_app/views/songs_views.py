from rest_framework.decorators import api_view
from rest_framework.response import Response
from spotify_app.models import Song, Artist
from spotify_app.serializers.song_serializer import * 
import random
from rest_framework import status
from spotify_app.serializers.artist_serializer import ArtistCustomSerializer
from random import shuffle

@api_view(['GET'])
def get_random_songs(request):
    song_ids = list(Song.objects.values_list('song_id', flat=True))  # ✅ use 'song_id' not 'id'
    random_ids = random.sample(song_ids, min(20, len(song_ids)))
    songs = Song.objects.filter(song_id__in=random_ids).select_related('artist')  # ✅ removed 'album'
    serializer = RandomSongSerializer(songs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_song_details(request, song_id):
    try:
        song = Song.objects.select_related('artist').get(song_id=song_id)  # ✅ removed 'album'
        print(song)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SongDetailSerializer(song)
    return Response(serializer.data)

@api_view(['GET'])
def artist_info_with_random_songs(request, artist_id):
    try:
        artist = Artist.objects.get(artist_id=artist_id)
        serializer = ArtistCustomSerializer(artist)
        return Response(serializer.data)
    except Artist.DoesNotExist:
        return Response({"error": "Artist not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def songs_by_artist(request, artist_id):
    try:
        artist = Artist.objects.get(artist_id=artist_id)
    except Artist.DoesNotExist:
        return Response({'error': 'Artist not found'}, status=status.HTTP_404_NOT_FOUND)

    # ✅ Sorted by popularity (descending)
    songs = Song.objects.filter(artist=artist).order_by('-popularity')

    serializer = SongSimpleSerializer(songs, many=True)
    return Response(serializer.data)