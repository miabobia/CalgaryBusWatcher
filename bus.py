# realtime positions taken from 
# https://data.calgary.ca/Transportation-Transit/Calgary-Transit-Realtime-Vehicle-Positions-GTFS-RT/am7c-qe3u/about_data
from dataclasses import dataclass

@dataclass
class Bus:
    position: tuple[float, float] # latitude, longitude
    timestamp: int
    vehicle_id: str
    trip_id: str
    name: str