#converting json text to python array

import json

file_path = 'C:/UW/4B/MTE482/path_info.txt'
product_id = ""
x = ""
y = ""
location_x = ""
location_y = ""
SCALE_X = 80
SCALE_Y = 80

with open(file_path, 'r') as file:
    path_info = json.load(file)

for entry in path_info:
    if product_id == "":
        product_id = entry.get("product_id", "N/A")
    if x == "":
        x = entry.get("x", "N/A")
    if y == "":
        y = entry.get("y", "N/A")
    location_x = entry.get("location_x", "N/A")
    location_y = entry.get("location_y", "N/A")

print(f"Product: {product_id}, x: {x}, y: {y}, X Loc: {location_x}, Y Loc: {location_y}")

def coord_conversion(loc_x, loc_y):
    #convert based on distance and map to grid
    #exact location provided from localization, so divide by size of grid
    location_x = location_x / SCALE_X
    location_y = location_y / SCALE_Y

