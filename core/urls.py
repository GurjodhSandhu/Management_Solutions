from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("truck/",views.truck,name="truck"),
    path("driver/",views.driver,name="driver"),
    path("truck/truck2", views.truck2, name="truck2"),

]