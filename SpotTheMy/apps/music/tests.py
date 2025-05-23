from django.test import TestCase

from recommendations.engine import recommend_for_user


class RecommendationsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user')
        self.artist = Artist.objects.create(name='Test Artist')
        self.track = Track.objects.create(title='Test', artist=self.artist, genre ='rock')

    def test_empty_history(self):
        recs = reccommend_for_user(self.user)
        self.assertEqual(len(recs), 10)