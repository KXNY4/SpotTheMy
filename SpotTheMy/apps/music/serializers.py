from rest_framework import serializers
from .models import Album, Track, Playlist, TrackReaction


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'
        read_only_fields = ['uploaded_by', 'created_at']

    def get_likes(self, obj):
        return obj.reactions.filter(reaction=TrackReaction.LIKE).count()
    
    def get_dislikes(self, obj):
        return obj.reactions.filter(reaction=TrackReaction.DISLIKE).count()


class TrackReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackReaction()
        fields = ['id', 'user', 'track', 'reaction', 'created_at']
        read_only_fields = ['user', 'created_at']

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