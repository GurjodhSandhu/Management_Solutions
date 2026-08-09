from django.db.models import Model
from django.shortcuts import render
from core.models import Truck, Driver


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
    truck = Truck.objects.get(id=id)
    return render(request,"truck_modify.html", {"truck": truck})

def driver_view(request):
    drivers = Driver.objects.all()
    return render(request, "driver.html",{"drivers": drivers})