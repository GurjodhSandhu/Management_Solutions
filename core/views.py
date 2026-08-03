from django.shortcuts import render
from core.models import Truck


# Create your views here.
def index(request):
    return render(request, 'home.html',
    )


def truck_view(request):
    trucks = Truck.objects.all()
    return render(request, "truck.html",{"trucks": trucks})