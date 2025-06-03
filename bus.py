# position: Tuple[lat, long]
# timestamp: str
# vehicle_id: str
# trip_id: str
# name: str -> taken from text files
from dataclasses import dataclass

@dataclass
class Bus:
    position: tuple[float, float] # latitude, longitude
    timestamp: int
    vehicle_id: str
    trip_id: str
    name: str