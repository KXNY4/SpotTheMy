from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings


class Album(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    audio_file = models.CharField(max_length=255, default='None')
    release_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return self.title


class Track(models.Model):
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='Track')
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="tracks/")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="tracks")
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_tracks", blank=True)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="playlist")
    tracks = models.ManyToManyField(Track, related_name="playlists")

    def __str__(self):
        return self.name



