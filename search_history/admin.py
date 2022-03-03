

from django.contrib import admin
from .models import SearchHistory

# Register your models here.

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'search_text', 'search_time')
    list_filter = ('user', 'search_time')
    search_fields = ('search_text', 'user__username')
    ordering = ('user',)



