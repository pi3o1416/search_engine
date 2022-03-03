

from django.urls import path
from . import views


app_name='search_history'
urlpatterns = [
    path('list/', views.SearchHistoryList.as_view(), name='list'),

]
