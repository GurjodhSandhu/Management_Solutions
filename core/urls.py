from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="home"),
    path("truck/",views.truck_view,name="truck"),
    path("driver/", views.driver_view, name="driver"),
    path("truck/<int:id>/",views.truck_modify,name="truck_modify"),

]