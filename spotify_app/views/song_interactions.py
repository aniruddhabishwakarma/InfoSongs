from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.songs_model import Like, Comment, Song
from ..serializers.song_interactions import LikeSerializer, CommentSerializer

# Like or Unlike a song
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_like(request, song_id):
    user = request.user
    try:
        song = Song.objects.get(song_id=song_id)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=404)

    like, created = Like.objects.get_or_create(user=user, song=song)
    if not created:
        like.delete()
        return Response({'message': 'Song unliked'}, status=200)
    return Response({'message': 'Song liked'}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_song_liked(request, song_id):
    liked = Like.objects.filter(user=request.user, song__song_id=song_id).exists()
    return Response({'liked': liked})

# Get all comments for a song
@api_view(['GET'])
def get_comments(request, song_id):
    comments = Comment.objects.filter(song__song_id=song_id).order_by('-timestamp')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, song_id):
    try:
        song = Song.objects.get(song_id=song_id)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=404)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, song=song)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# ✅ Delete Comment
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, user=request.user)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response({'message': 'Comment deleted'}, status=status.HTTP_204_NO_CONTENT)


# ✅ Edit/Update Comment
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id, user=request.user)
    except Comment.DoesNotExist:
        return Response({'error': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(comment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
