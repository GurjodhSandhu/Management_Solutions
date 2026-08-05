from django.db.models import Model
from django.shortcuts import render
from core.models import Truck, Driver


# Create your views here.
def index(request):
    return render(request, 'home.html',
    )

def truck_view(request):
    trucks = Truck.objects.all() #queryset (list) of truck objects
    return render(request, "truck.html",{"trucks": trucks}) #sends truck objects in trucks

def driver_view(request):
    drivers = Driver.objects.all()
    return render(request, "driver.html",{"drivers": drivers})