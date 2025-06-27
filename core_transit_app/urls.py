from django.urls import path
from . import views

urlpatterns = [
    path('core_transit_app/', views.core_transit_app, name='core_transit_app')
    # path('api/routes/', views.RouteViewSet.as_view(), name='route-list'),
    # path('api/trips/', views.TripViewSet.as_view(), name='trip-list'),
    # path('api/bus/', views.BusViewSet.as_view(), name='bus-list'),
]
