from django.urls import path
from .views.songs_views import *
from .views.auth_views import *
from .views.user_views import *

urlpatterns = [
    path('random-songs/', get_random_songs, name='random-songs'),
    path('song-details/<str:song_id>/', get_song_details, name='song-details'),
    path('artist/<str:artist_id>/', artist_info_with_random_songs),
    path('google-login/', GoogleLoginAPIView.as_view(), name='google-login'),
    path('profile/', user_profile),
    path('songs/artist/<str:artist_id>/', songs_by_artist, name='songs-by-artist'),
]