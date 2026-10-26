from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="home"),
    path("truck/",views.truck_view,name="truck"),
    path("driver/", views.driver_view, name="driver"),
    path("trip/", views.trip_view, name="trip"),
    path("truck/<int:id>/",views.truck_modify,name="truck_modify"),
    path("driver/<int:id>/",views.driver_modify,name="driver_modify"),
    path("trip/<int:id>/", views.trip_modify, name="trip_modify"),
    path("trip_action/<int:id>/", views.trip_action, name="trip_action"),

]