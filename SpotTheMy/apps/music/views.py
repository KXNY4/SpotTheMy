# from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Album, Track, Playlist, TrackReaction
from .serializers import AlbumSerializer, TrackSerializer, PlaylistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['artist', 'release_date']
    search_fields = ['title', 'artist']
    ordering_fields = ['release_date', 'title']


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['album']
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        track = self.get_object()
        TrackReaction.objects.update_or_create(
            user=request.user,
            track=track,
            defaults={'reaction': TrackReaction.LIKE}
        )
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        track = self.get_object()
        TrackReaction.objects.update_or_create(
            user=request.user,
            track=track,
            defaults={'reaction': TrackReaction.DISLIKE}
        )
        return Response({'status': 'disliked'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_reaction(self, request, pk=None):
        track = self.get_object()
        TrackReaction.objects.filter(user=request.user, track=track).delete()
        return Response({'status': 'reaction removed'}, status=status.HTTP_200_OK)



class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer