import re
import math

def obtener_coordenadas(linea):
    """
    Extract latitude, longitude, and yaw from the input line using regex.
    """
    lat_match = re.search(r"\[latitude: ([\d.-]+)\]", linea)
    lon_match = re.search(r"\[longitude: ([\d.-]+)\]", linea)
    yaw_match = re.search(r"\[.*yaw\s*:\s*([\d.-]+)", linea, re.IGNORECASE)  # Searches for 'yaw' in a flexible way
    
    if not (lat_match and lon_match and yaw_match):
        raise ValueError("Failed to extract coordinates and yaw from the input line.")
    
    latitud = float(lat_match.group(1))
    longitud = float(lon_match.group(1))
    yaw = float(yaw_match.group(1))
    
    print(latitud)
    print(longitud)
    print(yaw)
    
    return longitud, latitud, yaw


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two geographic points using the Haversine formula.
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Earth radius in meters
    R = 6371000  
    return R * c

def identificar_colector(lon, lat, yaw, filename="./MODULOS/mapas/extre2.txt"):
    """
    Identify the closest location based purely on Haversine distance.
    """
    closest_location = None
    min_distance = float('inf')

    with open(filename, 'r') as file:
        for line in file:
            loc_lat, loc_lon, loc_id = line.strip().split(', ')
            loc_lon = float(loc_lon)
            loc_lat = float(loc_lat)

            # Calculate Haversine distance between the current location and the location in the file
            distance = haversine_distance(lat, lon, loc_lat, loc_lon)
            # Find the location with the smallest distance
            if distance < min_distance:
                min_distance = distance
                closest_location = loc_id

    return closest_location
