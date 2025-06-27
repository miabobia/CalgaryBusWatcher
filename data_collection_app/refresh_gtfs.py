'''
refresh_gtfs.py

for repopulating CT_GTFS table
'''

import csv
import enum
import os
from core_transit_app.models import Route, Trip
from dotenv import load_dotenv
import time
from django.db import transaction
if os.path.isfile('.env'):
    load_dotenv('.env')

class TripsLegend(enum.Enum):
    ROUTE_ID = 0
    SERVICE_ID = 1
    TRIP_ID = 2
    TRIP_HEADSIGN = 3
    DIRECTION_ID = 4
    BLOCK_ID = 5
    SHAPE_ID = 6

class RoutesLegend(enum.Enum):
    ROUTE_ID = 0
    ROUTE_SHORT_NAME = 1
    ROUTE_LONG_NAME = 2
    ROUTE_DESC = 3
    ROUTE_TYPE = 4
    ROUTE_URL = 5
    ROUTE_COLOR = 6
    ROUTE_TEXT_COLOR = 7

def parse_text(file_path: str) -> list:
    # print('parsing textfile:', file_path)
    reader: csv._reader
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        # print(list(reader)[:5])
        return list(reader)[1:]

def insert_into_trip(data: list):
    print(f'INSERT_INTO_TRIP(): {time.asctime()}')
    for row in data:
        try:
            route_instance = Route.objects.get(route_id=row[TripsLegend.ROUTE_ID.value])
            # print(f'creating route instance!: {route_instance}')
        except Route.DoesNotExist:
            print(f"Route with ID {row[TripsLegend.ROUTE_ID.value]} does not exist. Skipping trip.")
        t = Trip(
            route = route_instance,
            service_id = row[TripsLegend.SERVICE_ID.value],
            trip_id = row[TripsLegend.TRIP_ID.value],
            trip_headsign = row[TripsLegend.TRIP_HEADSIGN.value],
            direction_id = row[TripsLegend.DIRECTION_ID.value],
            block_id = row[TripsLegend.BLOCK_ID.value],
            shape_id = row[TripsLegend.SHAPE_ID.value]
        )
        # print('TRIP:', t.__dict__)
        t.save()
    print(f'FINISHED UPDATING TRIP TABLE: {time.asctime()}')


def insert_into_route(data: list):
    print(f'INSERT_INTO_ROUTE(): {time.asctime()}')
    for row in data:
        r = Route(
            route_id = row[RoutesLegend.ROUTE_ID.value],
            # agency_id = row[RoutesLegend.AGENCY_ID.value],
            route_short_name = row[RoutesLegend.ROUTE_SHORT_NAME.value],
            route_long_name = row[RoutesLegend.ROUTE_LONG_NAME.value],
            route_desc = row[RoutesLegend.ROUTE_DESC.value],
            route_type = row[RoutesLegend.ROUTE_TYPE.value],
            route_url = row[RoutesLegend.ROUTE_URL.value],
            route_color = row[RoutesLegend.ROUTE_COLOR.value],
            route_text_color = row[RoutesLegend.ROUTE_TEXT_COLOR.value]
        )
        r.save()
    print(f'FINISHED UPDATING ROUTE TABLE: {time.asctime()}')

def bulk_insert_routes(data: list, batch_size: int = 1000):
    """Insert routes using bulk_create for better performance"""
    print(f'BULK_INSERT_ROUTES(): {time.asctime()}')
    
    routes_to_create = []
    for row in data:
        route = Route(
            route_id=row[RoutesLegend.ROUTE_ID.value],
            route_short_name=row[RoutesLegend.ROUTE_SHORT_NAME.value],
            route_long_name=row[RoutesLegend.ROUTE_LONG_NAME.value],
            route_desc=row[RoutesLegend.ROUTE_DESC.value],
            route_type=row[RoutesLegend.ROUTE_TYPE.value],
            route_url=row[RoutesLegend.ROUTE_URL.value],
            route_color=row[RoutesLegend.ROUTE_COLOR.value],
            route_text_color=row[RoutesLegend.ROUTE_TEXT_COLOR.value]
        )
        routes_to_create.append(route)
        
        # Insert in batches to avoid memory issues
        if len(routes_to_create) >= batch_size:
            Route.objects.bulk_create(routes_to_create, ignore_conflicts=True)
            routes_to_create = []
    
    # Insert remaining routes
    if routes_to_create:
        Route.objects.bulk_create(routes_to_create, ignore_conflicts=True)
    
    print(f'FINISHED BULK INSERT ROUTES: {time.asctime()}')

def bulk_insert_trips(data: list, batch_size: int = 1000):
    """Insert trips using bulk_create with optimized route lookups"""
    print(f'BULK_INSERT_TRIPS(): {time.asctime()}')
    
    route_ids = set(row[TripsLegend.ROUTE_ID.value] for row in data)

    routes_dict = {
        route.route_id: route 
        for route in Route.objects.filter(route_id__in=route_ids)
    }
    
    trips_to_create = []
    skipped_count = 0
    
    for row in data:
        route_id = row[TripsLegend.ROUTE_ID.value]
        
        if route_id not in routes_dict:
            print(f"Route with ID {route_id} does not exist. Skipping trip.")
            skipped_count += 1
            continue
        
        trip = Trip(
            route=routes_dict[route_id],
            service_id=row[TripsLegend.SERVICE_ID.value],
            trip_id=row[TripsLegend.TRIP_ID.value],
            trip_headsign=row[TripsLegend.TRIP_HEADSIGN.value],
            direction_id=row[TripsLegend.DIRECTION_ID.value],
            block_id=row[TripsLegend.BLOCK_ID.value],
            shape_id=row[TripsLegend.SHAPE_ID.value]
        )
        trips_to_create.append(trip)

        # Insert in batches
        if len(trips_to_create) >= batch_size:
            Trip.objects.bulk_create(trips_to_create, ignore_conflicts=True)
            trips_to_create = []
    
    if trips_to_create:
        Trip.objects.bulk_create(trips_to_create, ignore_conflicts=True)
    
    if skipped_count > 0:
        print(f'Skipped {skipped_count} trips due to missing routes')
    
    print(f'FINISHED BULK INSERT TRIPS: {time.asctime()}')

def update_tables():
    with transaction.atomic():
        Trip.objects.all().delete()
        Route.objects.all().delete()
        bulk_insert_routes(parse_text('/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS/routes.txt'))
        # insert_into_route(parse_text('/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS/routes.txt'))
        # print(f'\n\ninserting into trips at {time.asctime()}')
        # insert_into_trip(parse_text('/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS/trips.txt'))
        bulk_insert_trips(parse_text('/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS/trips.txt'))
        # print(f'finished inserting into trips at {time.asctime()}\n')
