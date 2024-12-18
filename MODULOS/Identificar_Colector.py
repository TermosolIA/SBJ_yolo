import re
from geopy.distance import geodesic

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

def obtener_hora(linea):
    """
    Extract time from the input line (first part before the comma).
    """
    return linea.split(',')[0]

def geodesic_distance(lat1, lon1, lat2, lon2):
    """
    Use geodesic distance calculation from geopy to measure the distance
    between two geographic points accurately.
    """
    return geodesic((lat1, lon1), (lat2, lon2)).meters

def identificar_colector(lon, lat, yaw, filename="./MODULOS/mapas/extre2.txt"):
    """
    Identify the closest location based purely on geodesic distance.
    """
    closest_location = None
    min_distance = float('inf')

    with open(filename, 'r') as file:
        for line in file:
            loc_lat, loc_lon, loc_id = line.strip().split(', ')
            loc_lon = float(loc_lon)
            loc_lat = float(loc_lat)

            # Calculate geodesic distance between the current location and the location in the file
            distance = geodesic_distance(lat, lon, loc_lat, loc_lon)
            # Find the location with the smallest distance
            if distance < min_distance:
                min_distance = distance
                closest_location = loc_id

    return closest_location
