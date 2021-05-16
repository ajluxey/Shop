from django.shortcuts import render
from django.views.generic import View

# Create your views here.


class TestView(View):
    def get(self, request):
        return render(request, 'testmodule/test.html')
