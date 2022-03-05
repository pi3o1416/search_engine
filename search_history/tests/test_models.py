
from django.test import TestCase
from search_history.models import SearchHistory, KeywordOccurences
from django.contrib.auth import get_user_model
from django.utils import timezone
import json


User = get_user_model()


class TestSearchHistory(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='shifat',
            email='shifat@gmail.com',
            password='shifat123',
        )
        self.history = SearchHistory.objects.create(
            user=self.user,
            search_text='ukraine current situation',
            search_time=timezone.now(),
            search_result=json.dumps({'hello': 'world'})
        )

    def test_search_text_label(self):
        self.assertEqual(self.history._meta.get_field('search_text').verbose_name, 'Search text')

    def test_search_text_max_length(self):
        self.assertEqual(self.history._meta.get_field('search_text').max_length, 200)

    def test_search_text_black_state(self):
        self.assertEqual(self.history._meta.get_field('search_text').blank, False)

    def test_search_time_label(self):
        self.assertEqual(self.history._meta.get_field('search_time').verbose_name, 'Search time')

    def test_search_result_label(self):
        self.assertEqual(self.history._meta.get_field('search_result').verbose_name, 'Search result')

    def test_get_absolute_url(self):
        self.assertEqual(self.history.get_absolute_url(), '/history/detail/{}/'.format(self.history.pk))


    class TestKeywordsOccurence(TestCase):
        def setUp(self):
            self.user = User.objects.create_user(
                username='shifat',
                email='shifat@gmail.com',
                password='shifat123',
            )
            self.history = SearchHistory.objects.create(
                user=self.user,
                search_text='ukraine current situation',
                search_time=timezone.now(),
                search_result=json.dumps({'hello': 'world'})
            )

        def test_autometic_generation(self):
            date = timezone.now().date()
            keywords = KeywordOccurences.objects.get(date=date)
            self.assertTrue(keywords)

        def test_date_lable(self):
            date = timezone.now().date()
            keywords = KeywordOccurences.objects.get(date=date)
            self.assertEqual(keywords._meta.get_field('date').verbose_name, 'Date')













