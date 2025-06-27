from .gtfs_realtime_pb2 import FeedMessage
from google.protobuf import message
from .bus import Bus
from core_transit_app.models import Bus as bus_model

def read_protobuf(file_path: str) -> "FeedMessage":
    feed = FeedMessage()
    with open(file_path, 'rb') as f:
        data = f.read()
        feed.ParseFromString(data)
    return feed

def fetch_route_name(trip_id: int) -> tuple[str, str]:

    lines = []
    with open('CT_GTFS/trips.txt', 'r') as f:
        lines = list(map(lambda x: x.split(','), f.read().splitlines()))
    
    lines = sorted(lines[1:], key=lambda x: int(x[2]))
    
    print(lines[0:5])

    return ('', '')

def read_vehicle_positions(feed: "FeedMessage"):

    def valid_vehicle(v):
        return v.HasField('vehicle') and v.HasField('trip')

    bus_list = []
    # for vehicle in map(lambda x: x.vehicle, filter(valid_vehicle, feed.entity)):
    for vehicle in map(lambda x: x.vehicle, filter(lambda x: x.HasField('vehicle'), feed.entity)):
        # print("Vehicle ID:", vehicle.vehicle.id, type(vehicle.vehicle.id))
        # print("Trip ID:", vehicle.trip.trip_id, type(vehicle.trip.trip_id))
        # print("Route ID:", vehicle.trip.route_id, type(vehicle.trip.route_id))
        # print("Latitude:", vehicle.position.latitude, type(vehicle.position.latitude))
        # print("Longitude:", vehicle.position.longitude)
        # print("Timestamp:", vehicle.timestamp, type(vehicle.timestamp))
        # print("---")

        short_name = ''
        bus_list.append(Bus(
            position=[
                vehicle.position.latitude,
                vehicle.position.longitude
            ],
            timestamp=vehicle.timestamp,
            vehicle_id=vehicle.vehicle.id,
            trip_id=vehicle.trip.trip_id,
            name=short_name
        ))
    
    update_bus_table(bus_list)

def update_bus_table(bus_list: list[Bus]):
    bus_model.objects.all().delete()
    print(f'saving bus position data to table: {bus_list[1]}')
    for bus in bus_list:
        b = bus_model(
            latitude=bus.position[0],
            longitude=bus.position[1],
            timestamp=bus.timestamp,
            vehicle_id=bus.vehicle_id,
            name=bus.name
        )
        b.save()