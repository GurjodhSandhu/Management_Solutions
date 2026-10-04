from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, DriverViewSet, TripViewSet

router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'trips', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
]