from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Home page")

def posts(request):
    return HttpResponse("Posts page")

def post(request, slug):
    return HttpResponse("individual post")