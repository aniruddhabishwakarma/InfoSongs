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



@api_view(['GET'])
def combined_search_view(request):
    query = request.GET.get("q", "").strip()

    if not query:
        return Response({"artists": [], "songs": []}, status=status.HTTP_200_OK)

    # Tokens from query (e.g., ["nirvana", "katy", "perry"])
    tokens = query.lower().split()

    # 🔍 Exact artist match (first priority)
    exact_artist = Artist.objects.filter(name__iexact=query).first()
    if exact_artist:
        top_songs = Song.objects.filter(artist=exact_artist).order_by("-popularity")[:5]
        albums = Song.objects.filter(artist=exact_artist).values_list("album_name", flat=True).distinct()[:5]

        return Response({
            "exact_artist": {
                "id": exact_artist.id,
                "name": exact_artist.name,
                "picture_url": exact_artist.picture_url,
                "genres": exact_artist.genres,
                "followers": exact_artist.followers,
                "popularity": exact_artist.popularity
            },
            "songs_by_artist": [
                {
                    "id": song.song_id,
                    "title": song.title,
                    "album_name": song.album_name,
                    "cover_url": song.cover_url
                } for song in top_songs
            ],
            "albums_by_artist": list(albums)
        })

    # 🔍 Exact song match (second priority)
    exact_song = Song.objects.filter(title__iexact=query).first()
    if exact_song:
        artist = exact_song.artist
        related_songs = Song.objects.filter(artist=artist).exclude(song_id=exact_song.song_id).order_by("-popularity")[:5]

        return Response({
            "exact_song": {
                "id": exact_song.song_id,
                "title": exact_song.title,
                "album_name": exact_song.album_name,
                "cover_url": exact_song.cover_url,
                "explicit": exact_song.explicit,
                "artist": {
                    "id": artist.id,
                    "name": artist.name,
                    "picture_url": artist.picture_url
                }
            },
            "related_songs": [
                {
                    "id": song.song_id,
                    "title": song.title,
                    "album_name": song.album_name,
                    "cover_url": song.cover_url
                } for song in related_songs
            ]
        })

    # 🧠 Multi-token match for partials
    artist_query = Q()
    song_query = Q()

    for word in tokens:
        artist_query |= Q(name__icontains=word)
        song_query |= Q(title__icontains=word)

    matched_artists = Artist.objects.filter(artist_query)
    matched_songs = Song.objects.filter(song_query)

    # Merge artists from song matches
    song_artists = {song.artist for song in matched_songs}
    all_artists = set(matched_artists) | song_artists

    return Response({
        "artists": [
            {
                "id": artist.id,
                "name": artist.name,
                "picture_url": artist.picture_url
            } for artist in all_artists
        ],
        "songs": [
            {
                "id": song.song_id,
                "title": song.title,
                "artist": song.artist.name,
                "album_name": song.album_name,
                "cover_url": song.cover_url
            } for song in matched_songs
        ]
    }, status=status.HTTP_200_OK)


    

