

from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import SearchHistory


class SearchHistoryList(View):
    query_set = SearchHistory.objects.all()
    template_name = 'searchHistory/list.html'

    def get(self, request):
        paginator = Paginator(self.query_set, 3)
        page = request.GET.get('page')
        try:
            searched_items = paginator.page(page)
        except PageNotAnInteger:
            searched_items = paginator.page(1)
        except EmptyPage:
            searched_items = paginator.page(paginator.num_pages)
        return render(request, self.template_name, {'searched_items': searched_items})


    def post(self, request):
        pass


class SearchHistoryDetail(View):
    template_name = 'searchHistory/detail.html'

    def get(self, request, pk):
        searched_item = SearchHistory.objects.get(pk=pk)
        return render(request,  self.template_name, {'searched_item': searched_item})





