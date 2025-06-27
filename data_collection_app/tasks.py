# cron jobs will be in here
'''
data_collection_app/tasks.py
'''
import os
import shutil
from core_transit_app.models import Route
import datetime
from .utils import download_file, unzip_file, hash_file
from .refresh_gtfs import update_tables
from .translate_vehicle_positions import read_protobuf, read_vehicle_positions
import time


TEMP_PATH = '/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/TEMP_CT_GTFS.zip'
GTFS_PATH = '/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS.zip'
GTFS_URL = 'https://data.calgary.ca/download/npk7-z3bj/application/zip'
GTFS_OUTPUT_DIR = '/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/CT_GTFS'

VEHICLE_POSITIONS_URL = "https://data.calgary.ca/download/am7c-qe3u/application/octet-stream"
VEHICLE_POSITIONS_PATH = "/home/mia_bobia/Documents/bus_tracker/bus_tracker_project/data_collection_app/vehiclepositions.pb"

def example_task():
    print(f'creating example_task_file.txt at {datetime.date()} - {datetime.time()}')
    with open('example_task_file.txt', 'w') as f:
        f.write("THIS IS AN EXAMPLE TASK")

def update_route_table():
    print(f'updating route table at {datetime.date()} - {datetime.time()}')
    r = Route(route_id=5)
    r.save()

def delete_dir(dir: str):
    try:
        shutil.rmtree(dir)
        print(f'removed directory {dir}')
    except OSError as e:
        print(f'Error: {e.filename} - {e.strerror}.')

def update_gtfs():
    print(f'UPDATE_GTFS(): {time.asctime()}')
    download_file(GTFS_URL, TEMP_PATH)
    gtfs_hash = hash_file(GTFS_PATH)
    temp_gtfs_hash = hash_file(TEMP_PATH)

    # ct_gtfs.zip does not need to be updated
    # if gtfs_hash == temp_gtfs_hash:
    if False:
        print(f'hashes match nothing being overwritten!')
        # print(f'{TEMP_PATH} hash == {GTFS_PATH} hash !')
        os.remove(TEMP_PATH)
        return

    # remove existing ct_gtfs.zip and extracted directory
    os.remove(GTFS_PATH)
    print(f'removing {GTFS_PATH}')
    delete_dir(GTFS_OUTPUT_DIR)
    os.rename(TEMP_PATH, GTFS_PATH)
    print(f'renamed {TEMP_PATH} to {GTFS_PATH}')

    unzip_file(GTFS_PATH, GTFS_OUTPUT_DIR)
    update_tables()
    # after we extract file we need to use its contents to fill out model (refresh_gtfs.py)
    delete_dir(GTFS_OUTPUT_DIR)
    # after thatttt we delete unzipped dir

def update_bus_position():
    print(f'UPDATE_BUS_POSITION(): {time.asctime()}')

    # download bus positions
    download_file(VEHICLE_POSITIONS_URL, VEHICLE_POSITIONS_PATH)

    # overwrite bus position
    read_vehicle_positions(read_protobuf(VEHICLE_POSITIONS_PATH))
