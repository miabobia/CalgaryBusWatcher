from django.urls import path
from . import views

urlpatterns = [
    path('core_transit_app/', views.core_transit_app, name='core_transit_app'),
    path('api/routes/', views.RouteListAPIView.as_view(), name='route-list'),
    path('api/routes/<str:route_id>/', views.RouteDetailAPIView.as_view(), name='route-detail'),
    path('api/trips/', views.TripListAPIView.as_view(), name='trip-list'),
    # path('api/trips/<str:route_id>/', views.RouteDetailAPIView.as_view(), name='route-detail'),
]
