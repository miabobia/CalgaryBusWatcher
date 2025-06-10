from django.urls import path
from . import views

urlpatterns = [
    path('core_transit_app/', views.core_transit_app, name='core_transit_app'),
]
