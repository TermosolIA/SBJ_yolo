import pandas as pd
import folium

# File path
file_path = 'extre2.txt'  # Replace with the actual path to your file

# Step 1: Read the file into a DataFrame
df = pd.read_csv(file_path, header=None, names=['latitude', 'longitude', 'label'])

# Step 2: Create a Folium map centered around the average coordinates
center_lat = df['latitude'].mean()
center_lon = df['longitude'].mean()
map_obj = folium.Map(location=[center_lat, center_lon], zoom_start=15)

# Step 3: Add markers to the map
for _, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=row['label']
    ).add_to(map_obj)

# Step 4: Save the map to an HTML file
map_obj.save('map.html')

print("Map has been saved as map.html")
