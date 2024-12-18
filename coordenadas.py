import math
import folium

# Constants
EARTH_RADIUS = 6378137  # Earth's radius in meters

def calculate_new_coordinates(lat, long, distance_north, distance_east):
    delta_lat = distance_north / EARTH_RADIUS
    delta_long = distance_east / (EARTH_RADIUS * math.cos(math.pi * lat / 180))
    
    new_lat = lat + (delta_lat * 180 / math.pi)
    new_long = long + (delta_long * 180 / math.pi)
    
    return new_lat, new_long

def calculate_bearing(lat1, lon1, lat2, lon2):
    d_lon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(d_lon))
    
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    
    return compass_bearing

def calculate_destination_point(lat, lon, bearing, distance):
    lat = math.radians(lat)
    lon = math.radians(lon)
    bearing = math.radians(bearing)

    lat2 = math.asin(math.sin(lat) * math.cos(distance / EARTH_RADIUS) +
                     math.cos(lat) * math.sin(distance / EARTH_RADIUS) * math.cos(bearing))
    lon2 = lon + math.atan2(math.sin(bearing) * math.sin(distance / EARTH_RADIUS) * math.cos(lat),
                            math.cos(distance / EARTH_RADIUS) - math.sin(lat) * math.sin(lat2))
    
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    
    return lat2, lon2

def map_solar_plant(num_rows, row_separation, panel_separation, hallways, hallway_ends, letters):
    panel_coordinates = []
    
    for i, (start, end) in enumerate(zip(hallways, hallway_ends)):
        start_lat, start_long = start
        end_lat, end_long = end
        bearing = calculate_bearing(start_lat, start_long, end_lat, end_long)
        total_distance = math.sqrt((end_lat - start_lat)**2 + (end_long - start_long)**2) * EARTH_RADIUS
        
        north_letter, south_letter = letters[i]
        north_coords = []
        south_coords = []
        
        for row in range(num_rows):
            distance_along_hallway = row * row_separation
            if distance_along_hallway > total_distance:
                break
            
            hallway_lat, hallway_long = calculate_destination_point(start_lat, start_long, bearing, distance_along_hallway)
            north_panel_lat, north_panel_long = calculate_new_coordinates(hallway_lat, hallway_long, panel_separation / 2, 0)
            south_panel_lat, south_panel_long = calculate_new_coordinates(hallway_lat, hallway_long, -panel_separation / 2, 0)
            north_coords.append((north_panel_lat, north_panel_long, f"{north_letter}{row + 1}"))
            south_coords.append((south_panel_lat, south_panel_long, f"{south_letter}{row + 1}"))
            
        panel_coordinates.append((north_coords, south_coords))
    
    return panel_coordinates

def calculate_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon1])
    d_lat = lat2 - lat1
    d_lon = lon2 - lon1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = EARTH_RADIUS * c
    return distance

def find_closest_panel(drone_lat, drone_long, panel_coords):
    closest_coord = None
    min_distance = float('inf')
    
    for north_coords, south_coords in panel_coords:
        for coord in north_coords + south_coords:
            row_lat, row_long, letter = coord
            distance = calculate_distance(drone_lat, drone_long, row_lat, row_long)
            if distance < min_distance:
                min_distance = distance
                closest_coord = coord
                
    return closest_coord

def create_map(panel_coords, hallway_coords, drone_coord, closest_coord, output_file):
    plant_map = folium.Map(location=hallway_coords[0], zoom_start=18)
    all_coordinates = []

    for north_coords, south_coords in panel_coords:
        for coord in north_coords:
            folium.Marker(location=(coord[0], coord[1]), icon=folium.Icon(color='blue', icon='glyphicon glyphicon-th'), popup=coord[2]).add_to(plant_map)
            all_coordinates.append(coord)
        for coord in south_coords:
            folium.Marker(location=(coord[0], coord[1]), icon=folium.Icon(color='blue', icon='glyphicon glyphicon-th'), popup=coord[2]).add_to(plant_map)
            all_coordinates.append(coord)
            
        # folium.Marker(location=(drone_coord[0], drone_coord[1]), icon=folium.Icon(color='red', icon='glyphicon glyphicon-th'), popup=coord[2]).add_to(plant_map)
        # folium.Marker(location=(closest_coord[0], closest_coord[1]), icon=folium.Icon(color='red', icon='glyphicon glyphicon-th'), popup=coord[2]).add_to(plant_map)
    with open(output_file, 'w') as file:
        for coord in all_coordinates:
            file.write(f"{coord[0]}, {coord[1]}, {coord[2]}\n")
    
    return plant_map

# Example usage
num_rows = 84
row_separation = 17.21  # 17.2 meters between each row
panel_separation = 80 # Configurable distance between north and south panels

hallways = [(38.622555,-6.754470),(38.62531,-6.75432),(38.62819,-6.75425),(38.63104,-6.75419),(38.63381,-6.75410)]  # Example starting hallway coordinates
hallway_ends = [(38.62224,-6.73790),(38.62499,-6.73790),(38.62788,-6.73779),(38.63073,-6.73773),(38.63347,-6.73758)]  # Example ending hallway coordinates
letters = [('A', 'A'),('C', 'B'),('E', 'D'),('G', 'F'),('H', 'H')]  # Letters for north and south groups in each hallway

panel_coords = map_solar_plant(num_rows, row_separation, panel_separation, hallways, hallway_ends, letters)

# Drone parameters
drone_coord = (38.63701,-6.75579)  # Example drone coordinate

# Find the closest panel
closest_coord = find_closest_panel(drone_coord[0], drone_coord[1], panel_coords)

# Extract hallway coordinates for the map
hallway_coords = hallways

# Create the map and save points to a text file
output_file = 'solar_plant_points.txt'
plant_map = create_map(panel_coords, hallway_coords, drone_coord, closest_coord, output_file)

# Save the map to an HTML file
plant_map.save('solar_plant_map.html')

# Display the map in a Jupyter Notebook (if applicable)
plant_map
