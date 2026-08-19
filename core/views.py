from copyreg import constructor

from django.core.exceptions import ValidationError
from django.shortcuts import render
from core.models import Truck, Driver, Trip
from .services.service_driver import update_driver
from .services.service_truck import update_truck
from .services.service_trip import update_trip
from .repositories import TruckRepository, TripRepository, DriverRepository

# Create your views here.
def index(request):
    return render(request, 'home.html',
    )

def truck_view(request):
    context = {}
    trucks = TruckRepository.get_all_trucks() #queryset (list) of truck objects
    context["trucks"]=trucks
    return render(request, "truck/truck.html", {'trucks': trucks}) #sends truck objects in trucks

def truck_modify(request,id):
    context = {}
    truck = TruckRepository.get_truck(id)
    context["truck"] = truck
    if request.method == "POST":
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        try:
            context["truck"] = update_truck(truck.id,data)
            context["message"] = "success"
        except ValidationError as e:
            context["message"] = e
    return render(request,"truck/truck_modify.html", context)

def driver_view(request):
    drivers = DriverRepository.get_all_drivers()
    return render(request, "driver/driver.html",{"drivers": drivers})

def driver_modify(request,id):
    context = {}
    driver = DriverRepository.get_driver(id)
    context["driver"] = DriverRepository.get_driver(id)
    context["trucks"]= TruckRepository.get_all_trucks()
    if request.method == "POST":
        data = request.POST.dict()
        try:
            context['driver'] = update_driver(driver.id,data)
            context["message"] = "success"
        except ValidationError as e:
            context["message"] = e

    return render(request,"driver/driver_modify.html", context)

def trip_view(request):
    trip = TripRepository.get_all_trips()
    return render(request, "trip/trip.html",{"trips": trip})

def trip_modify(request,id):
    context = {}
    trip = TripRepository.get_trip(id)
    context["trip"] = trip
    context["drivers"]= DriverRepository.get_all_drivers()
    if request.method == "POST":
        data = request.POST.dict()
        try:
            context["trip"] = update_trip(id,data)
            context["message"] = "success"
        except ValidationError as e:
            context["message"] = e
    return render(request,"trip/trip_modify.html", context)