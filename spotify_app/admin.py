from django.contrib import admin
from .models.songs_model import *
from .models.auth_model import *

admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(CustomUser)
admin.site.register(Like)
admin.site.register(Comment)
