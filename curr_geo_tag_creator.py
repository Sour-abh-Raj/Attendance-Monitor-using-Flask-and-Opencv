import csv
import geocoder

def get_loc_tag_name():
    print("Enter the name of the location tag you want to create.")
    tag = str(input("Location tag name: "))
    return tag

def generate_current_location_tag():
    g = geocoder.ip('me')
    print(f"Current location: {g.city}, {g.state}")
    print(f"Latitude: {g.latlng[0]}")
    print(f"Longitude: {g.latlng[1]}")
    tag =get_loc_tag_name()
    if g.latlng:
        return [(tag, g.latlng[0], g.latlng[1])]
    else:
        return []

def save_tags_to_csv(tags, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Location', 'Latitude', 'Longitude'])
        writer.writerows(tags)
    print(f"Geolocation tag saved to {filename}.")

def main():
    tags = generate_current_location_tag()
    save_tags_to_csv(tags, 'current_location_tag.csv')
    
if __name__ == '__main__':
    main()
