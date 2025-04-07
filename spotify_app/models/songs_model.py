from django.db import models

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
    cover_url = models.URLField(blank=True, null=True)  # ✅ Add this!
