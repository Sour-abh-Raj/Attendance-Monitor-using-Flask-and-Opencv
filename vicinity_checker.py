import csv
import geopy.distance
import geocoder

def check_location_in_vicinity(vicinity, csv_file):
    g = geocoder.ip('me')
    if not g.latlng:
        return False
    
    current_location = (g.latlng[0], g.latlng[1])
    print(f"Current location: {current_location}")

    with open(csv_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            location = row[0]
            latitude = float(row[1])
            longitude = float(row[2])
            location_coordinates = (latitude, longitude)
            
            distance = geopy.distance.distance(current_location, location_coordinates).m
            print(f"Distance from {location} to current location is {distance:.2f} meters.")
            if distance <= vicinity:
                return True

    return False

