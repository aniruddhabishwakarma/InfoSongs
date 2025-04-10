from django.urls import path
from .views.songs_views import *
from .views.auth_views import *
from .views.user_views import *
from .views.song_interactions import *

urlpatterns = [
    path('random-songs/', get_random_songs, name='random-songs'),
    path('song-details/<str:song_id>/', get_song_details, name='song-details'),
    path('artist/<str:artist_id>/', artist_info_with_random_songs),
    path('google-login/', GoogleLoginAPIView.as_view(), name='google-login'),
    path('auth/signup/', SignupAPIView.as_view(), name='signup'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('profile/', user_profile),
    path('songs/artist/<str:artist_id>/', songs_by_artist, name='songs-by-artist'),
    path('songs/<str:song_id>/like/', toggle_like, name='toggle-like'),
    path('songs/<str:song_id>/comments/', get_comments, name='get-comments'),
    path('songs/<str:song_id>/comments/add/', add_comment, name='add-comment'),
    path('songs/<str:song_id>/is-liked/', is_song_liked, name='is-song-liked'),
    path('comments/<int:comment_id>/delete/', delete_comment, name='delete-comment'),
    path('comments/<int:comment_id>/edit/', edit_comment, name='edit-comment'),
    path('playlists/', user_playlists, name='user-playlists'),
    path('playlists/create/', create_playlist, name='create-playlist'),
    path('playlists/<int:playlist_id>/', playlist_detail, name='playlist-detail'),
    path('playlists/<int:playlist_id>/add/', add_song_to_playlist, name='add-song'),
    path('playlists/<int:playlist_id>/remove/<str:song_id>/', remove_song_from_playlist, name='remove-song'),
    path('playlists/<int:playlist_id>/delete/', delete_playlist, name='delete-playlist'),
     path('liked-songs/', liked_songs, name='liked-songs'),
]