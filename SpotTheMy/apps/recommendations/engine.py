from collections import Counter
from django.db.models import Count
from django.core.cache import cache


def reccommend_for_user(user):
    history = user.listening_history.select_related('track__artist', 'track__genre').all()

    if not history:
        return Track.objects.annotate(likes=Count('reactions')).order_by('-likes')[:10]
    
    top_genres = Counter([h.track.genre for h in history]).most_common(3)
    top_artists = Counter([h.track.artits_id for h in history]).most_common(2)

    return Track.objects.filter(models.Q(genre__in=[g for g, cnt in top_genres]) | models.Q(artist_id__in=[a for a, cnt in top_artists])).exclude(id__in=[h.track_id for h in history]).order_by('?')[:15]

def get_chached_recommentations(user):
    cach_key = f'user_{user.id}_recs'
    recs = cache.get(cache_key)
    
    if not recs:
        recs = reccommend_for_user(user)
        cache.set(cache_key, recs, timeout=3600)
    
    return recs