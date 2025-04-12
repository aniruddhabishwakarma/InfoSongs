from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from ..models.user_model import *
from ..models.songs_model import *
from ..serializers.playlist_serializer import PlaylistSerializer, PlaylistDetailSerializer
from spotify_app.serializers.user_serializer import UserProfileSerializer
from ..serializers.song_serializer import SongDetailSerializer  # adjust this path as needed



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    print("🔥 USER ID:", request.user.id)

    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)

# Create a new playlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_playlist(request):
    name = request.data.get('name')
    description = request.data.get('description', '')

    if not name:
        return Response({"error": "Playlist name is required."}, status=400)

    playlist = Playlist.objects.create(user=request.user, name=name, description=description)
    return Response(PlaylistSerializer(playlist).data, status=201)

# Get all playlists for the logged-in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_playlists(request):
    playlists = Playlist.objects.filter(user=request.user).order_by('-created_at')
    serializer = PlaylistSerializer(playlists, many=True)
    return Response(serializer.data)

# View songs inside a playlist
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def playlist_detail(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
    except Playlist.DoesNotExist:
        return Response({"error": "Playlist not found"}, status=404)

    # Get songs in the playlist
    playlist_songs = PlaylistSong.objects.filter(playlist=playlist).select_related('song__artist')

    # Extract only the songs, then serialize using SongDetailsSerializer
    songs = [ps.song for ps in playlist_songs]

    

    song_data = SongDetailSerializer(songs, many=True).data

    return Response({
        "playlist_id": playlist.id,
        "playlist_name": playlist.name,
        "songs": song_data
    })


# Add a song to a playlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_song_to_playlist(request, playlist_id):
    song_id = request.data.get('song_id')
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        song = Song.objects.get(song_id=song_id)
        PlaylistSong.objects.get_or_create(playlist=playlist, song=song)
        return Response({"message": "Song added"})
    except Playlist.DoesNotExist:
        return Response({"error": "Playlist not found"}, status=404)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"}, status=404)

# Remove a song from a playlist
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_song_from_playlist(request, playlist_id, song_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        song = Song.objects.get(song_id=song_id)
        PlaylistSong.objects.filter(playlist=playlist, song=song).delete()
        return Response({"message": "Song removed"})
    except Playlist.DoesNotExist:
        return Response({"error": "Playlist not found"}, status=404)
    except Song.DoesNotExist:
        return Response({"error": "Song not found"}, status=404)

# Delete a playlist
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_playlist(request, playlist_id):
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=request.user)
        playlist.delete()
        return Response({"message": "Playlist deleted"})
    except Playlist.DoesNotExist:
        return Response({"error": "Playlist not found"}, status=404)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_search_keyword(request):
    keyword = request.data.get("keyword", "").strip()
    exact_song_id = request.data.get("song_id")
    exact_artist_id = request.data.get("artist_id")

    if not keyword:
        return Response({"error": "Invalid keyword"}, status=400)

    history, created = SearchHistory.objects.get_or_create(
        user=request.user,
        keyword=keyword,
        defaults={
            "is_exact_song": bool(exact_song_id),
            "is_exact_artist": bool(exact_artist_id),
            "song_id": exact_song_id,
            "artist_id": exact_artist_id,
        }
    )
    return Response({"success": True})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_search_history(request):
    history = SearchHistory.objects.filter(user=request.user).select_related("song", "artist")[:10]
    data = []

    for item in history:
        entry = {
            "id": item.id,
            "keyword": item.keyword,
            "type": "song" if item.is_exact_song else "artist" if item.is_exact_artist else "text"
        }

        if item.is_exact_song and item.song:
            entry.update({
                "title": item.song.title,
                "artist": item.song.artist.name,
                "cover_url": item.song.cover_url
            })
        elif item.is_exact_artist and item.artist:
            entry.update({
                "artist_name": item.artist.name,
                "picture_url": item.artist.picture_url
            })

        data.append(entry)

    return Response(data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_search_keyword(request, pk):
    try:
        keyword = SearchHistory.objects.get(id=pk, user=request.user)
        keyword.delete()
        return Response({"success": True})
    except SearchHistory.DoesNotExist:
        return Response({"error": "Keyword not found"}, status=404)
    

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def clear_search_history(request):
    SearchHistory.objects.filter(user=request.user).delete()
    return Response({"success": True})


