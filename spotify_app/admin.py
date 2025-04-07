from django.contrib import admin
from .models.songs_model import Artist, Song
from .models.auth_model import *

admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(CustomUser)
