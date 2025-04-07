import csv
from django.core.management.base import BaseCommand
from spotify_app.models import Song

class Command(BaseCommand):
    help = 'Import songs from songs.csv into the database'

    def handle(self, *args, **kwargs):
        file_path = 'songs.csv'  # Assuming it's in the root folder

        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                count = 0
                for row in reader:
                    _, created = Song.objects.update_or_create(
                        uri=row['uri'],
                        defaults={
                            'title': row['title'],
                            'artist': row['artist'],
                            'album': row['album'],
                            'album_cover': row['album_cover'],
                            'duration_ms': int(row['duration_ms']),
                        }
                    )
                    count += 1

                self.stdout.write(self.style.SUCCESS(f"🎉 {count} songs imported from {file_path}"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"❌ File not found: {file_path}"))

