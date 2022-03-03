

from django.shortcuts import render
from django.views import View
from .models import SearchHistory


class SearchHistoryList(View):

    query_set = SearchHistory.objects.all()
    template_name = 'searchHistory/list.html'

    def get(self, request):
        return render(request, self.template_name, {'searched_items': self.query_set})

    def post(self, request):
        pass




