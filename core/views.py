from copyreg import constructor

from django.shortcuts import render
from core.models import Truck, Driver, Trip
from .services.service_driver import update_driver
from .services.service_truck import update_truck
from .services.service_trip import update_trip


# Create your views here.
def index(request):
    return render(request, 'home.html',
    )

def truck_view(request):
    context = {}
    trucks = Truck.objects.all() #queryset (list) of truck objects
    context["trucks"]=trucks

    return render(request, "truck/truck.html",context) #sends truck objects in trucks

def truck_modify(request,id):
    context = {}
    truck = Truck.objects.get(id=id)
    context["truck"] = truck
    if request.method == "POST":
        vin = request.POST.get("vin")
        brand = request.POST.get("brand")
        year = request.POST.get("year")
        mileage = request.POST.get("mileage")
        truck_status = request.POST.get("truck_status")
        truck_location = request.POST.get("truck_location")
        data = {"vin":vin,
                "brand":brand,
                "year":year,
                "mileage":mileage,
                "truck_status":truck_status,
                "truck_location":truck_location}
        try:
            update_truck(truck.id,data)
            context["message"] = "success"
            context["truck"] = Truck.objects.get(id=id)
        except Exception as e:
            context["message"] = e
    return render(request,"truck/truck_modify.html", context)

def driver_view(request):
    drivers = Driver.objects.all()
    return render(request, "driver/driver.html",{"drivers": drivers})

def driver_modify(request,id):
    context = {}
    driver = Driver.objects.get(id=id)
    context["driver"] = driver
    context["trucks"]=Truck.objects.all()
    if request.method == "POST":
        driver_name = request.POST.get("driver_name")
        driver_licensenumber = request.POST.get("driver_licensenumber")
        truck = request.POST.get("truck")

        try:
            update_driver(driver.id,{
                    "driver_name":driver_name,
                    "driver_licensenumber":driver_licensenumber,
                    "truck":Truck.objects.get(id=truck)
            })
            context["message"] = "success"
            context["driver"] = Driver.objects.get(id=id)
        except Exception as e:
            context["message"] = e

    return render(request,"driver/driver_modify.html", context)

def trip_view(request):
    trip = Trip.objects.all()
    return render(request, "trip/trip.html",{"trips": trip})

def trip_modify(request,id):
    context = {}
    trip = Trip.objects.get(id=id)
    context["trip"] = trip
    context["drivers"]=Driver.objects.all()
    if request.method == "POST":
        start = request.POST.get("start")
        end = request.POST.get("end")
        arrival_time = request.POST.get("arrival_time")
        departure_time = request.POST.get("departure_time")
        planned_miles = request.POST.get("planned_miles")
        cpm = request.POST.get("cpm")
        driver = request.POST.get("driver")
        try:
            update_trip(id,{
                "start":start,
                "end":end,
                "arrival_time":arrival_time,
                "departure_time":departure_time,
                "planned_miles":planned_miles,
                "cpm":cpm,
                "driver":Driver.objects.get(id=driver)
                            })
            context["trip"] = Trip.objects.get(id=id)
            context["message"] = "success"
        except Exception as e:
            context["message"] = e
    return render(request,"trip/trip_modify.html", context)