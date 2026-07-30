from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
    return HttpResponse("homepage.")

def truck(request):
    return HttpResponse("truck")

def truck2(request):
    return HttpResponse("truck2")

def driver(request):
    return HttpResponse("driver")