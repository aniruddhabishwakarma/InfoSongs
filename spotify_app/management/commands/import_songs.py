# spotify_app/management/commands/import_songs.py
import os
import requests
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from spotify_app.models.songs_model import Song

class Command(BaseCommand):
    help = 'Update album names for existing songs using Spotify API'

    def handle(self, *args, **options):
        load_dotenv()
        
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        token = self.get_spotify_token(client_id, client_secret)
        if not token:
            self.stdout.write(self.style.ERROR('❌ Failed to get Spotify access token'))
            return

        songs = Song.objects.all()
        for song in songs:
            if not song.album_name:
                album_name = self.fetch_album_name(song.uri, token)
                song.album_name = album_name or 'Single'
                song.save()
                self.stdout.write(self.style.SUCCESS(f"✅ {song.title} → {album_name}"))

    def get_spotify_token(self, client_id, client_secret):
        url = "https://accounts.spotify.com/api/token"
        data = {'grant_type': 'client_credentials'}
        auth = (client_id, client_secret)
        res = requests.post(url, data=data, auth=auth)
        if res.status_code == 200:
            return res.json()['access_token']
        return None

    def fetch_album_name(self, track_uri, token):
        track_id = track_uri.split(':')[-1]
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        headers = {'Authorization': f'Bearer {token}'}
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            return data.get('album', {}).get('name', 'Single')
        return 'Single'
