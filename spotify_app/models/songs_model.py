from django.db import models
from .auth_model import CustomUser  # ✅ Directly import your custom user model

class Artist(models.Model):
    artist_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    genres = models.JSONField(default=list, blank=True)
    followers = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    picture_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    song_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    duration = models.IntegerField()
    uri = models.CharField(max_length=255)
    explicit = models.BooleanField()
    popularity = models.IntegerField(default=0)
    cover_url = models.URLField(blank=True, null=True)
    album_name = models.CharField(max_length=255, blank=True, null=True)  # 👈 Add this

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ✅ Correct reference
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'song')

    def __str__(self):
        return f"{self.user.username} liked {self.song.title}"


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ✅ Correct reference
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.given_name} on {self.song.title}"
