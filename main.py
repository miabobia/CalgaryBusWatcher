import gtfs_realtime_pb2
from google.protobuf import message
import bus

def read_protobuf(file_path: str) -> gtfs_realtime_pb2.FeedMessage:
    feed = gtfs_realtime_pb2.FeedMessage()
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

def read_vehicle_positions(feed: gtfs_realtime_pb2.FeedMessage):

    busses = []
    for vehicle in map(lambda x: x.vehicle, filter(lambda x: x.HasField('vehicle'), feed.entity)):
        print("Vehicle ID:", vehicle.vehicle.id, type(vehicle.vehicle.id))
        print("Trip ID:", vehicle.trip.trip_id, type(vehicle.trip.trip_id))
        print("Route ID:", vehicle.trip.route_id, type(vehicle.trip.route_id))
        print("Latitude:", vehicle.position.latitude, type(vehicle.position.latitude))
        print("Longitude:", vehicle.position.longitude)
        print("Timestamp:", vehicle.timestamp, type(vehicle.timestamp))
        print("---")

        short_name = ''
        b = bus.Bus(
            position=[
                vehicle.position.latitude,
                vehicle.position.longitude
            ],
            timestamp=vehicle.timestamp,
            vehicle_id=vehicle.vehicle_id,
            trip_id=vehicle.trip.trip_id,
            name=short_name
            

        )

    # print(len(vehicle_ids), len(set(vehicle_ids)))
# Example usage:
# read_vehicle_positions(read_protobuf("vehiclepositions.pb"))
fetch_route_name('')


# TODAY:

# make a Bus class that has the following attrs
# position: Tuple[lat, long]
# timestamp: str
# vehicle_id: str
# trip_id: str
# name: str -> taken from text files
