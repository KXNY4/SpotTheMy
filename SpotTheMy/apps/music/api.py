from rest_framework.decorators import api_view
from rest_framework.response import Response
from SpotTheMy.apps.music.models import Track
from serializers import TrackSerializer



@api_view(['GET'])
def user_recommendations(request):
    from recommendations import reccommend_for_user
    tracks = reccommend_for_user(request.user)
    return Response({
        'user': request.user.username,
        'recommendations': TrackSerializer(tracks, many=True).data
    })


@api_view(['GET'])
def optimized_tracks(request):
    tracks = Track.objects.select_related('artist').prefetch_related('reactions').only('title', 'artist__name', 'duration')[:50]
    return Response(TrackSerializer(tracks, many=True).data)