
from django.shortcuts import render
from django.views import View

# Create your views here.


class HomePage(View):
    template_name = 'home/home.html'
    def get(self, request):
        return render(request, self.template_name)



