import requests
import time
import os
import base64
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from spotify_app.models.songs_model import Artist, Song

# Load credentials
load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

ARTIST_NAMES = [
    "Nepathya",
    "1974 AD",
    "Albatross",
    "Anuprastha",
    "Cobweb",
    "The Shadows",
    "The Edge Band",
    "Mukti and Revival",
    "The Uglyz",
    "Mantra",
    "Tribal Rain"
]

def get_access_token():
    auth_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    res = requests.post(auth_url, headers=headers, data=data)
    res.raise_for_status()
    return res.json()["access_token"]

class Command(BaseCommand):
    help = 'Fetch artist and top 50 song data from Spotify API (no albums)'

    def handle(self, *args, **options):
        token = get_access_token()
        headers = {"Authorization": f"Bearer {token}"}

        for name in ARTIST_NAMES:
            print(f"\n🔍 Searching for artist: {name}")
            artist_data = self.search_artist(name, headers)
            if not artist_data:
                print(f"❌ Artist not found: {name}")
                continue

            artist_obj, _ = Artist.objects.update_or_create(
                artist_id=artist_data["id"],
                defaults={
                    "name": artist_data["name"],
                    "genres": artist_data.get("genres", []),
                    "followers": artist_data["followers"]["total"],
                    "popularity": artist_data["popularity"],
                    "picture_url": artist_data["images"][0]["url"] if artist_data["images"] else ""
                }
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Artist saved: {artist_obj.name}"))

            songs = self.get_all_tracks(artist_data["id"], headers)[:50]
            for i, song in enumerate(songs):
                Song.objects.update_or_create(
                    song_id=song["id"],
                    defaults={
                        "title": song["name"],
                        "artist": artist_obj,
                        "duration": song["duration_ms"],
                        "uri": song["uri"],
                        "explicit": song["explicit"],
                        "popularity": song.get("popularity", 0),
                        "cover_url": song["album"]["images"][0]["url"] if song["album"]["images"] else ""
                    }
)
                if i % 10 == 0: time.sleep(0.3)

    def search_artist(self, name, headers):
        url = f"https://api.spotify.com/v1/search?q={name}&type=artist&limit=1"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            items = res.json().get("artists", {}).get("items", [])
            return items[0] if items else None
        return None

    def get_all_tracks(self, artist_id, headers):
        tracks = []
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?include_groups=album,single,compilation&limit=20"
        seen_track_ids = set()

        while url and len(tracks) < 100:
            res = requests.get(url, headers=headers)
            if res.status_code != 200:
                break
            data = res.json()
            albums = data["items"]
            for album in albums:
                album_tracks_url = f"https://api.spotify.com/v1/albums/{album['id']}/tracks?limit=50"
                track_res = requests.get(album_tracks_url, headers=headers)
                if track_res.status_code == 200:
                    album_tracks = track_res.json().get("items", [])
                    for track in album_tracks:
                        if track["id"] not in seen_track_ids:
                            seen_track_ids.add(track["id"])
                            full_track = self.get_track_details(track["id"], headers)
                            if full_track:
                                tracks.append(full_track)
                if len(tracks) >= 50:
                    break
                time.sleep(0.2)
            url = data.get("next")
        return tracks

    def get_track_details(self, track_id, headers):
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.json()
        return None
