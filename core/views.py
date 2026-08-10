from copyreg import constructor

from django.shortcuts import render
from core.models import Truck, Driver
from .services.service_driver import update_driver
from .services.service_truck import update_truck


# Create your views here.
def index(request):
    return render(request, 'home.html',
    )

def truck_view(request):
    context = {}
    if request.method == "POST":
        tid = request.POST.get("tid")
        lname = request.POST.get("lname")
        context["tid"] = tid
        context["lname"] = lname

    trucks = Truck.objects.all() #queryset (list) of truck objects
    context["trucks"]=trucks

    return render(request, "truck.html",context) #sends truck objects in trucks

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
    return render(request,"truck_modify.html", context)

def driver_view(request):
    drivers = Driver.objects.all()
    return render(request, "driver.html",{"drivers": drivers})

def driver_modify(request,id):
    context = {}
    driver = Driver.objects.get(id=id)
    context["driver"] = driver
    if request.method == "POST":
        driver_name = request.POST.get("driver_name")
        driver_licensenumber = request.POST.get("driver_licensenumber")
        try:
            update_driver(driver.id,{"driver_name":driver_name,"driver_licensenumber":driver_licensenumber})
            context["message"] = "success"
            context["driver"] = Driver.objects.get(id=id)
        except Exception as e:
            context["message"] = e

    return render(request,"driver_modify.html", context)
