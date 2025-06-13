from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import generics
from rest_framework.response import Response
from .models import Route, Trip
from .serializers import RouteSerializer, TripSerializer


class RouteListAPIView(generics.ListAPIView):
    """Get all routes"""
    queryset = Route.objects.all()
    serializer_class = RouteSerializer


class RouteDetailAPIView(generics.RetrieveAPIView):
    """Get a single route by route_id"""
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    lookup_field = 'route_id'  # Use route_id instead of default 'pk'

class TripListAPIView(generics.ListAPIView):
    """Get all routes"""
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

# class RouteDetailAPIView(generics.RetrieveAPIView):
#     """Get a single route by route_id"""
#     queryset = Route.objects.all()
#     serializer_class = RouteSerializer
#     lookup_field = 'route_id'  # Use route_id instead of default 'pk'

def core_transit_app(request):
    template = loader.get_template('myfirst.html')
    return HttpResponse(template.render())