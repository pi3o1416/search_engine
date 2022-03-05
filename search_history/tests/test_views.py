

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from search_history.models import SearchHistory, KeywordOccurences
import json


User = get_user_model()
class TestListHistory(TestCase):
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


    def test_if_url_exist_in_desire_url(self):
        response = self.client.get('/history/list/')
        self.assertEqual(response.status_code, 200)


    def test_if_url_accessable_by_name(self):
        response = self.client.get(reverse('search_history:list'))
        self.assertEqual(response.status_code, 200)


class TestHistoryDetail(TestCase):
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

    def test_if_url_exist_in_desire_url(self):
        response = self.client.get('/history/detail/{}/'.format(self.history.pk))
        self.assertEqual(response.status_code, 200)

    def test_if_url_accessable_by_name(self):
        response = self.client.get(reverse('search_history:detail', args=[self.history.pk]))
        self.assertEqual(response.status_code, 200)


