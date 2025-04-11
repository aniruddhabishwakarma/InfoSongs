# spotify_app/models/user_model.py

from django.db import models
from django.conf import settings
from .songs_model import Song

User = settings.AUTH_USER_MODEL

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} by {self.user}"

class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='songs')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('playlist', 'song')

    def __str__(self):
        return f"{self.song.title} in {self.playlist.name}"
    
# models/search_history.py

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    is_exact_artist = models.BooleanField(default=False)
    is_exact_song = models.BooleanField(default=False)
    song = models.ForeignKey("Song", null=True, blank=True, on_delete=models.SET_NULL)
    artist = models.ForeignKey("Artist", null=True, blank=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "keyword")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user.email} - {self.keyword}"

