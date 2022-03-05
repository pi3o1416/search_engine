
from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user_model
from functools import reduce
from operator import __and__
from collections import defaultdict
import json
import itertools
from .models import SearchHistory, KeywordOccurences



class SearchHistoryList(View):
    query_set = SearchHistory.objects.all().order_by('-search_time')
    users = get_user_model().objects.all()[:10]
    template_name = 'searchHistory/list.html'
    keywords_dict = top_searched_keywords()

    def get(self, request):
        self.query_set = self.get_queryset(request.GET)
        paginator = Paginator(self.query_set, 3)
        page = request.GET.get('page')
        try:
            searched_items = paginator.page(page)
        except PageNotAnInteger:
            searched_items = paginator.page(1)
        except EmptyPage:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return HttpResponse('')
            searched_items = paginator.page(paginator.num_pages)

        # Keep only top ten searched keywords
        self.keywords_dict = dict(
            itertools.islice(self.keywords_dict.items(), 10))

        # if ajax request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render( request, 'searchHistory/content_list.html', { 'searched_items': searched_items })
        return render(
            request,
            self.template_name,
            {
                'searched_items': searched_items,
                'top_keywords': self.keywords_dict,
                'users': self.users
            }
        )

    def get_queryset(self, data):
        history_filters = []
        keyword_filters = []
        startDate = timezone.now().date() - timezone.timedelta(days=30)
        endDate = timezone.now().date()
        # filter based on search field
        if data.get('search'):
            history_filters.append(
                Q(search_text__icontains=data.get('search')))
        # filter based on top keywords
        if data.get('top_keywords'):
            history_filters.append(
                Q(search_text__icontains=data.get('top_keywords')))
        # filter based on user
        if data.get('users'):
            history_filters.append(Q(user__id=data.get('users')))
        # filter based on Date select
        if data.get('date_from'):
            startDate = timezone.datetime.strptime(
                data.get('date_from'), '%Y-%m-%d')
        if data.get('date_to'):
            endDate = timezone.datetime.strptime(
                data.get('date_to'), '%Y-%m-%d')
        # filter based on date range
        if data.get('time_range'):
            time_range = data.get('time_range')
            if time_range == '24h':
                startDate = endDate - timezone.timedelta(days=1)
            elif time_range == '7d':
                startDate = endDate - timezone.timedelta(days=7)
            elif time_range == '1m':
                startDate = endDate - timezone.timedelta(days=30)

        history_filters.append(Q(search_time__gte=startDate))
        history_filters.append(Q(search_time__lte=endDate))

        keyword_filters.append(Q(date__gte=startDate))
        keyword_filters.append(Q(date__lte=endDate))


        self.keywords_dict = top_searched_keywords(keyword_filters)
        return SearchHistory.objects.filter(reduce(__and__, history_filters)).order_by('-search_time')


    def top_searched_keywords(self, filters=None, time_range=False):
        """
        Return Top 10 searched keywords within a timerange
        if time_range is False return top searched keywords within last month
        """
        if not time_range:
            firstDate = timezone.now().date() - timezone.timedelta(days=30)
            lastDate = timezone.now().date()
            filters = [Q(date__gte=firstDate), Q(date__lte=lastDate)]
        query_set = KeywordOccurences.objects.filter(reduce(__and__, filters))
        keywords = defaultdict(int)

        for obj in query_set:
            obj_keywords = json.loads(obj.keywords)
            for key, val in obj_keywords.items():
                keywords[key] += val

        keywords = {key: value for key, value in sorted(
            keywords.items(), key=lambda item: item[1], reverse=True)}
        return keywords


class SearchHistoryDetail(View):
    template_name = 'searchHistory/detail.html'

    def get(self, request, pk):
        searched_item = SearchHistory.objects.get(pk=pk)
        return render(request,  self.template_name, {'searched_item': searched_item})
