from django.shortcuts import render_to_response
from django.http import HttpResponse

def home(request):
    """The home view"""
    return HttpResponse("hello world!")