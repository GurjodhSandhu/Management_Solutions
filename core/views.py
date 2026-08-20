from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from core.models import Truck, Driver, Trip
from .services import service_trip
from .services.service_driver import update_driver
from .services.service_truck import update_truck
from .services.service_trip import update_trip
from .repositories import TruckRepository, TripRepository, DriverRepository

# Create your views here.
def index(request):
    context = {}
    trips = TripRepository.get_all_trips()
    trucks = TruckRepository.get_all_trucks()
    drivers = DriverRepository.get_all_drivers()
    context["trips"] = trips
    context["trucks"] = trucks
    context["drivers"] = drivers
    return render(request, 'home.html', context)

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

def trip_action(request,id):
    context = {}
    trip = TripRepository.get_trip(id)
    if request.method == "POST":
        try:
            if request.POST["action"] == "trip_start":
                service_trip.start_trip(trip.id)
                messages.success(request, "Successfully Started")

            elif request.POST["action"] == "trip_complete":
                service_trip.complete_trip(trip.id)
                messages.success(request, "Successfully completed")
            elif request.POST["action"] == "trip_stop":
                service_trip.incomplete_trip(trip.id)
                messages.success(request, "Successfully stopped")

            elif request.POST["action"] == "trip_cancel":
                service_trip.cancel_trip(trip.id)
                messages.success(request, "Successfully cancelled")
        except ValidationError as e:
            messages.error(request, str(e))
    return redirect(request.META.get("HTTP_REFERER"))

