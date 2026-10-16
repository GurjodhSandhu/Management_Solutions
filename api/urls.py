from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TruckViewSet, DriverViewSet, TripViewSet, MeView

router = DefaultRouter()
router.register(r'trucks', TruckViewSet, basename='truck')
router.register(r'drivers', DriverViewSet, basename='driver')
router.register(r'trips', TripViewSet, basename='trip')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', MeView.as_view(), name='me'),
]