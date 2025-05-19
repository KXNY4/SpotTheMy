from dataclasses import fields
from tkinter import CASCADE
from django.db import models
from django.contrib.auth import get_user_model


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

class TrackReaction(models.Model):
    LIKE = 'like'
    DISLIKE = 'dislike'
    REACTION_CHOICES = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    track = models.ForeignKey('Track', on_delete=models.CASCADE, related_name='reactions')
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')

    def __str__(self):
        return f"{self.user} {self.reaction} {self.track}"


class Track(models.Model):
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='Track')
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(upload_to="tracks/")
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="tracks")

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


class ListeningHistory(models.Model):
    user = models.ForeignKey(get_user_model(), models.CASCADE, db_index=True)
    track = models.ForeignObject('Track', on_delete=CASCADE, db_index=True)
    listened_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.index(fields=['user', '-listened_at']),
        ]


