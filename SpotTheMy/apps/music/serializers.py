from rest_framework import serializers
from .models import Album, Track, Playlist


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'created_at']


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ["id", "title", "artist", "release_date", "user", "tracks"]


class PlaylistSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ["id", "name", "user", "tracks"]