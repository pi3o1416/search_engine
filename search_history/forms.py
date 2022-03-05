

from django import forms
from .models import SearchHistory


#This form is unused
class FilterForm(forms.ModelForm):
    class Meta:
        model = SearchHistory
        fields = ('user', 'search_time', 'search_text', )


