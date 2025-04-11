from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from ..models.user_model import Playlist, PlaylistSong
from ..models.songs_model import Song
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
