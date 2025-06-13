'''
refresh_gtfs.py

for repopulating CT_GTFS table
'''

import csv
import enum
import sqlite3
import os
from core_transit_app.models import Route, Trip
from dotenv import load_dotenv
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
    print('parsing textfile:', file_path)
    reader: csv._reader
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        # print(list(reader)[:5])
        return list(reader)[1:]

def insert_into_trip(data: list):
    print("INSERT INTO TRIP WITH DATA: ", data)
    for row in data:
        t = Trip(
            route = row[TripsLegend.ROUTE_ID.value],
            service_id = row[TripsLegend.SERVICE_ID.value],
            trip_id = row[TripsLegend.TRIP_ID.value],
            trip_headsign = row[TripsLegend.TRIP_HEADSIGN.value],
            direction_id = row[TripsLegend.DIRECTION_ID.value],
            block_id = row[TripsLegend.BLOCK_ID.value],
            shape_id = row[TripsLegend.SHAPE_ID.value]
        )
        print('TRIP:', t.__dict__)
        t.save()

def insert_into_route(data: list):
    for row in data:
        r = Route(
            route_id = row[RoutesLegend.ROUTE_ID.value],
            agency_id = row[RoutesLegend.AGENCY_ID.value],
            route_short_name = row[RoutesLegend.ROUTE_SHORT_NAME.value],
            route_long_name = row[RoutesLegend.ROUTE_LONG_NAME.value],
            route_desc = row[RoutesLegend.ROUTE_DESC.value],
            route_type = row[RoutesLegend.ROUTE_TYPE.value],
            route_url = row[RoutesLegend.ROUTE_URL.value],
            route_color = row[RoutesLegend.ROUTE_COLOR.value],
            route_text_color = row[RoutesLegend.ROUTE_TEXT_COLOR.value]
        )
        r.save()

def update_tables():
    print('update_tables()')
    Trip.objects.all().delete()
    Route.objects.all().delete()
    # insert_into_route(parse_text('/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS/routes.txt'))
    insert_into_trip(parse_text('/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS/trips.txt'))