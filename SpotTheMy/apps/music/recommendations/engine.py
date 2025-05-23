from collections import Counter
from django.db.models import Count
from django.core.cache import cache
from apps.music.models import Track, ListeningHistory


def recommend_for_user(user):
    try:
        if hasattr(user, 'listening_history'):
            history = user.listening_history.select_related('track__artist').all()
            if history.exists():
                top_artists = [h.track.artist_id for h in history]
                return Track.objects.filter(artist_id__in=top_artists).exclude(
                    id__in=[h.track_id for h in history]
                ).order_by('?')[:10]
    
        return Track.objects.annotate(likes=Count('reactions')).order_by('-likes')[:10]

    except Exception as e:
        print(f"Recommendation error: {e}")
        return Track.objects.none()

def get_chached_recommentations(user):
    cache_key = f'user_{user.id}_recs'
    recs = cache.get(cache_key)
    
    if not recs:
        recs = recommend_for_user(user)
        cache.set(cache_key, recs, timeout=3600)
    
    return recs