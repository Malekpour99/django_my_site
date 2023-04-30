from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def starting_page(request):
    return HttpResponse("Home page")

def posts(request):
    return HttpResponse("Posts page")

def post_detail(request, slug):
    return HttpResponse("individual post")