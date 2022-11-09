from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    return render(request, 'test/index.html')




# Create your views here.
