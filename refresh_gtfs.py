'''
refresh_gtfs.py

for repopulating CT_GTFS table
'''

import csv
import enum
import sqlite3
import os
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
    reader: csv._reader
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def clear_table(table_name: str, db: sqlite3.Connection):
    db.execute(f"DELETE FROM {table_name};")
    db.commit()

def build_trips_table(data: list, db: sqlite3.Connection):
    for row in data:
        db.execute(
            """
            INSERT INTO TRIPS
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (row[TripsLegend.ROUTE_ID.value],
                row[TripsLegend.SERVICE_ID.value],
                row[TripsLegend.TRIP_ID.value],
                row[TripsLegend.TRIP_HEADSIGN.value],
                row[TripsLegend.DIRECTION_ID.value],
                row[TripsLegend.BLOCK_ID.value],
                row[TripsLegend.SHAPE_ID.value]
            )
        )
    db.commit()

def build_routes_table(data: list, db: sqlite3.Connection):
    for row in data:
        db.execute(
            """
            INSERT INTO ROUTES
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row[RoutesLegend.ROUTE_ID.value],
                row[RoutesLegend.ROUTE_SHORT_NAME.value],
                row[RoutesLegend.ROUTE_LONG_NAME.value],
                row[RoutesLegend.ROUTE_DESC.value],
                row[RoutesLegend.ROUTE_TYPE.value],
                row[RoutesLegend.ROUTE_URL.value],
                row[RoutesLegend.ROUTE_COLOR.value],
                row[RoutesLegend.ROUTE_TEXT_COLOR.value]
            )
        )
    db.commit()

def refresh_tables(db: sqlite3.Connection):
    clear_table("TRIPS", db)
    build_trips_table(parse_text('CT_GTFS/trips.txt'), db)

    clear_table("ROUTES", db)
    build_routes_table(parse_text('CT_GTFS/routes.txt'), db)

def init_tables(db: sqlite3.Connection):
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS TRIPS(route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id)")
    cur.execute("CREATE TABLE IF NOT EXISTS ROUTES(route_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color)")
    cur.close()
    db.commit()

def get_db_reference() -> sqlite3.Connection:
    return sqlite3.connect(os.environ['DATABASE'])

# if __name__ == '__main__':
#     # print(parse_text('CT_GTFS/trips.txt')[0])

#     #['route_id', 'service_id', 'trip_id', 'trip_headsign', 'direction_id', 'block_id', 'shape_id']
# # route_id,route_short_name,route_long_name,route_desc,route_type,route_url,route_color,route_text_color

#     db = sqlite3.connect(os.environ['DATABASE'])
#     cur = db.cursor()
#     cur.execute("CREATE TABLE IF NOT EXISTS TRIPS(route_id, service_id, trip_id, trip_headsign, direction_id, block_id, shape_id)")
#     cur.execute("CREATE TABLE IF NOT EXISTS ROUTES(route_id, route_short_name, route_long_name, route_desc, route_type, route_url, route_color, route_text_color)")
#     cur.close()
#     db.commit()



