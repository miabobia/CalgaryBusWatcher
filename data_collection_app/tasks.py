# cron jobs will be in here
'''
data_collection_app/tasks.py
'''
import os
from core_transit_app.models import Route
import datetime

def example_task():
    print(f'creating example_task_file.txt at {datetime.date()} - {datetime.time()}')
    with open('example_task_file.txt', 'w') as f:
        f.write("THIS IS AN EXAMPLE TASK")

def update_route_table():
    print(f'updating route table at {datetime.date()} - {datetime.time()}')
    r = Route(route_id=5)
    r.save()