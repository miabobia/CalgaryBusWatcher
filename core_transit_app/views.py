from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from .models import Route, Trip, Bus
from .serializers import RouteSerializer, TripSerializer, BusSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().order_by('route_short_name')
    serializer_class = RouteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['route_short_name', 'route_long_name']

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all().order_by('vehicle_id')
    serializer_class = BusSerializer

def core_transit_app(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())